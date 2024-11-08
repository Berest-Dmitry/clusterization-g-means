from BusinessLogic.TransportModels.transport_message import TransportMessage
from typing import TypeVar, Generic

T = TypeVar("T")

class TransportMessageWithBody(TransportMessage, Generic[T]):
    MessageBody: T
