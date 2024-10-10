import string
from typing import List
import pika
import pydantic_xml
from Models.full_user_data_for_clustering import FullUserDataForClustering
from Models.transport_message import TransportMessage
from Models.transport_message_with_body import TransportMessageWithBody


class DataExtractor:
    rmq_conn_str: string = "localhost"
    rmq_params: pika.ConnectionParameters
    rmq_listener_connection: pika.BlockingConnection
    result_list: List[FullUserDataForClustering] = None


    def __init__(self):
        self.rmq_params = pika.ConnectionParameters(self.rmq_conn_str)
        self.rmq_listener_connection = pika.BlockingConnection(self.rmq_params)
        self.rmq_listener_channel = self.rmq_listener_connection.channel()
        self.rmq_listener_channel.queue_declare("CTQ", durable=True, exclusive=False, auto_delete=False)


    def BasicPuplish(self):
        request_connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        request_channel = request_connection.channel()
        request_channel.queue_declare("MyQueue", durable=False, auto_delete=False, exclusive=False)
        tm = TransportMessage(TransportMessageType=1,
                              TaskDescription=1,
                              MessageHeader="",
                              IsLastChunk=True)
        xml = tm.to_xml(
            encoding = "UTF-8",
        )
        request_channel.basic_publish("", routing_key="MyQueue", mandatory=True, body=xml)
        request_connection.close()


    def BasicConsume(self):
        def callback(ch, method, properties, body):
            if body is None:
                print("Failed to retrieve user data!")
            msg_body: TransportMessageWithBody[List[FullUserDataForClustering]] = body.decode('utf-8')
            result_list = msg_body.message_body
            if result_list is None or result_list.count() == 0:
                print("No data is present to process")
            return

        self.rmq_listener_channel.basic_consume(queue="CTQ", on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages')
        self.rmq_listener_channel.start_consuming()




