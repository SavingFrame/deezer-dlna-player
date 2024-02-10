from xml.etree import ElementTree as ET

from didl_lite.didl_lite import Resource


class CustomResource(Resource):
    def to_xml(self) -> ET.Element:
        attribs = {
            "protocolInfo": self.protocol_info or "",
            "duration": self.duration or "",
        }
        res_el = ET.Element("res", attribs)
        res_el.text = self.uri
        return res_el
