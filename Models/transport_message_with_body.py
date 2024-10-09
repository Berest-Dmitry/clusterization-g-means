from Models.transport_message import TransportMessage
from typing import TypeVar, Generic

T = TypeVar("T")

class TransportMessageWithBody(TransportMessage, Generic[T]):
    message_body: T

    def __init__(self, tmt, td, message_header, is_last_chunk, message_body: T):
        super().__init__(tmt, td, message_header, is_last_chunk)
        self.message_body = message_body