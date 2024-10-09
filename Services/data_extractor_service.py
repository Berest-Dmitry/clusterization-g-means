import string
from idlelib.iomenu import encoding

import pika
import pydantic_xml

from Models.transport_message import TransportMessage


class DataExtractor:
    rmq_conn_str: string = "localhost"
    rmq_params: pika.ConnectionParameters
    rmq_listener_connection: pika.BlockingConnection


    def __init__(self):
        self.rmq_params = pika.ConnectionParameters(self.rmq_conn_str)
        self.rmq_listener_connection = pika.BlockingConnection(self.rmq_params)
        self.rmq_listener_channel = self.rmq_listener_connection.channel()
        self.rmq_listener_channel.queue_declare("CTQ", durable=True, exclusive=False, auto_delete=False)


    def BasicPuplish(self):
        request_connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        request_channel = request_connection.channel()
        request_channel.queue_declare("MyQueue", durable=False, auto_delete=False, exclusive=False)
        tm = TransportMessage(1, 1, None, True)
        xml = tm.to_xml(
            encoding = "UTF-8",
        )

