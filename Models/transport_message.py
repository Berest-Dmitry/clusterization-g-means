from typing import Optional, Literal
from pydantic_xml import BaseXmlModel, attr


class TransportMessage(BaseXmlModel):
    TransportMessageType: Literal[int] = attr()
    TaskDescription: Literal[int] = attr()
    MessageHeader: Literal[int] = attr()
    IsLastChunk: Literal[bool] = attr()

    def __init__(self, tmt, td, message_header, is_last_chunk):
        super().__init__()
        self.TransportMessageType = tmt
        self.TaskDescription = td
        self.MessageHeader = message_header
        self.IsLastChunk = is_last_chunk