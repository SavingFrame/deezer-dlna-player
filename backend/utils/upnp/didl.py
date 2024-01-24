from xml.etree import ElementTree as ET

from didl_lite.didl_lite import Resource


class CustomResource(Resource):

    def to_xml(self) -> ET.Element:
        attribs = {
            "protocolInfo": self.protocol_info or "",
            "duration": self.duration or "",
            "albumArtURI": "https://e-cdns-images.dzcdn.net/images/cover/48a16c3faf45614021367b31c05d1b2e/250x250-000000-80-0-0.jpg"
        }
        res_el = ET.Element("res", attribs)
        res_el.text = self.uri
        return res_el
