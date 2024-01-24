from async_upnp_client.const import DeviceIcon
from pydantic import BaseModel, ConfigDict, Field, computed_field


class DlnaDeviceSchema(BaseModel):
    friendly_name: str
    manufacturer: str
    model_name: str
    icons: list[DeviceIcon] = Field(exclude=True)
    udn: str

    model_config = ConfigDict(from_attributes=True, protected_namespaces=('__',))

    @computed_field
    @property
    def icon(self) -> str:
        return self.icons[0].url
