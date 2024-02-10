import logging
from mimetypes import guess_type
from typing import Optional, Mapping, Any

from async_upnp_client.const import MIME_TO_UPNP_CLASS_MAPPING
from async_upnp_client.exceptions import UpnpError
from async_upnp_client.profiles.dlna import DmrDevice, _LOGGER, dlna_handle_notify_last_change
from async_upnp_client.utils import absolute_url
from didl_lite import didl_lite

from utils.upnp.didl import CustomResource

logger = logging.getLogger("upnp_listener")


class CustomDmrDevice(DmrDevice):
    def __init__(self, *args, **kwargs):
        self.on_queue_event = None
        super().__init__(*args, **kwargs)

    async def _get_mimetype_upnp_class_and_dlna_features(
        self,
        media_url: str,
        default_mime_type: Optional[str] = None,
        default_upnp_class: Optional[str] = None,
        override_mime_type: Optional[str] = None,
        override_upnp_class: Optional[str] = None,
        override_dlna_features: Optional[str] = None,
    ) -> tuple[str, str, str]:
        mime_type = override_mime_type or ""
        upnp_class = override_upnp_class or ""
        dlna_features = override_dlna_features or "*"

        if None in (override_mime_type, override_dlna_features):
            # do a HEAD/GET, to retrieve content-type/mime-type
            try:
                headers = await self._fetch_headers(media_url, {"GetContentFeatures.dlna.org": "1"})
                if headers:
                    if not override_mime_type and "Content-Type" in headers:
                        mime_type = headers["Content-Type"]
                    if not override_dlna_features and "ContentFeatures.dlna.org" in headers:
                        dlna_features = headers["ContentFeatures.dlna.org"]
            except Exception:  # pylint: disable=broad-except
                pass

            if not mime_type:
                _type = guess_type(media_url.split("?")[0])
                mime_type = _type[0] or ""
                if not mime_type:
                    mime_type = default_mime_type or "application/octet-stream"

            # use CM/GetProtocolInfo to improve on dlna_features
            if not override_dlna_features and dlna_features != "*" and self.has_get_protocol_info:
                protocol_info_entries = await self._async_get_sink_protocol_info_for_mime_type(mime_type)
                for entry in protocol_info_entries:
                    if entry[3] == "*":
                        # device accepts anything, send this
                        dlna_features = "*"

        # Try to derive a basic upnp_class from mime_type
        if not override_upnp_class:
            mime_type = mime_type.lower()
            for _mime, _class in MIME_TO_UPNP_CLASS_MAPPING.items():
                if mime_type.startswith(_mime):
                    upnp_class = _class
                    break
            else:
                upnp_class = default_upnp_class or "object.item"
        return mime_type, upnp_class, dlna_features

    async def construct_play_media_metadata(
        self,
        media_url: str,
        media_title: str,
        default_mime_type: Optional[str] = None,
        default_upnp_class: Optional[str] = None,
        override_mime_type: Optional[str] = None,
        override_upnp_class: Optional[str] = None,
        override_dlna_features: Optional[str] = None,
        meta_data: Optional[Mapping[str, Any]] = None,
    ) -> str:
        """
        Construct the metadata for play_media command.

        This queries the source and takes mime_type/dlna_features from it.

        The base metadata is updated with key:values from meta_data, e.g.
        `meta_data = {"artist": "Singer X"}`
        """
        # pylint: disable=too-many-arguments, too-many-locals, too-many-branches
        meta_data = meta_data or {}
        mime_type, upnp_class, dlna_features = await self._get_mimetype_upnp_class_and_dlna_features(
            media_url,
            default_mime_type=default_mime_type,
            default_upnp_class=default_upnp_class,
            override_mime_type=override_mime_type,
            override_upnp_class=override_upnp_class,
            override_dlna_features=override_dlna_features,
        )
        if meta_data:
            duration = meta_data.get("duration", None)
            album_art_uri = meta_data.get("albumArtURI", None)
        else:
            duration = None
            album_art_uri = None
        # build DIDL-Lite item + resource
        didl_item_type = didl_lite.type_by_upnp_class(upnp_class)
        if not didl_item_type:
            raise UpnpError("Unknown DIDL-lite type")

        protocol_info = f"http-get:*:{mime_type}:{dlna_features}"
        resource = CustomResource(uri=media_url, protocol_info=protocol_info, duration=duration)
        resources = [resource]
        if album_art_uri:
            album_mime_type, _, album_dlna_features = await self._get_mimetype_upnp_class_and_dlna_features(
                album_art_uri,
            )
            album_protocol_info = f"http-get:*:{album_mime_type}:{album_dlna_features}"
            album_picture = CustomResource(uri=album_art_uri, protocol_info=album_protocol_info)
            resources.append(album_picture)
        item = didl_item_type(
            id="0",
            parent_id="-1",
            title=media_title or meta_data.get("title"),
            restricted="false",
            resources=resources,
        )

        # Set any metadata properties that are supported by the DIDL item
        for key, value in meta_data.items():
            setattr(item, key, str(value))
        xml_string: bytes = didl_lite.to_xml_string(item)
        return xml_string.decode("utf-8")

    @property
    def media_image_url(self) -> Optional[str]:
        state_var = self._state_variable("AVT", "CurrentTrackMetaData")
        if state_var is None:
            return None

        xml = state_var.value
        if not xml or xml == "NOT_IMPLEMENTED":
            return None

        items = didl_lite.from_xml_string(xml, strict=False)
        if not items:
            return None

        device_url = self.profile_device.device_url
        for item in items:
            # Some players use Item.albumArtURI,
            # though not found in the UPnP-av-ConnectionManager-v1-Service spec.
            if hasattr(item, "album_art_uri"):
                return absolute_url(device_url, item.album_art_uri)

            for res in item.resources:
                protocol_info = res.protocol_info or ""
                if protocol_info.startswith("http-get:*:image/"):
                    return absolute_url(device_url, res.uri)

        return None

    @property
    def next_transport_uri(self) -> Optional[str]:
        """Check if device has controls to set the next item for playback."""
        state_var = self._state_variable("AVT", "NextAVTransportURI")
        value: Optional[str] = state_var.value
        if value is None:
            _LOGGER.debug("Got no value for Volume_mute")
            return None

        return value

    async def _on_queue_event(self, service_id: str, state_variables: list[dict]) -> None:
        """State variable(s) changed, perform callback(s)."""
        # handle DLNA specific event
        service = self.device.service_id(service_id)
        state_variables_class = []
        for state_variable_dict in state_variables:
            state_variable_name = state_variable_dict.get("name")
            state_variable_value = state_variable_dict.get("upnp_value")
            state_variable = service.state_variable(state_variable_name)
            state_variables_class.append(state_variable)
            state_variable.upnp_value = state_variable_value
            if state_variable.name == "LastChange":
                dlna_handle_notify_last_change(state_variable)
            if service_id == "urn:upnp-org:serviceId:AVTransport":
                if state_variable.name == "CurrentTrackMetaData":
                    self._update_current_track_meta_data(state_variable)
                if state_variable.name == "AVTransportURIMetaData":
                    self._update_av_transport_uri_metadata(state_variable)
        if self.on_queue_event:
            await self.on_queue_event(service, state_variables_class)
        logger.debug(f"Service {service_id} changed state_variables")
