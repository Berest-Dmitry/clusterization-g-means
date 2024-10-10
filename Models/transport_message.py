from typing import Optional
from pydantic import Field
from pydantic_xml import BaseXmlModel, attr, element


class TransportMessage(BaseXmlModel):
    TransportMessageType: Optional[int] = element(xml_attribute=True, default_factory=int, name="TransportMessageType")
    TaskDescription: Optional[int] = element(xml_attribute=True, default=None, name='TaskDescription')
    MessageHeader: Optional[str] = element(xml_attribute=True, default='', name='MessageHeader')
    IsLastChunk: Optional[bool] = element(xml_attribute=True, default_factory=bool, name='IsLastChunk')
