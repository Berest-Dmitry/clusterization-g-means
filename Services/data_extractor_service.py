import string
from typing import List
import pika
import xmltodict
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

    def ParseXML(self, xml_string: str):
        data_dict = xmltodict.parse(xml_string)
        transport_message_data = data_dict['TransportMessage']

        # обработка поля описания исполняемой задачи
        if 'TaskDescription' in transport_message_data:
            task_description_value = transport_message_data['TaskDescription']
            if (task_description_value is None or
                     task_description_value['@xsi:nil'] == 'true'):
                transport_message_data['TaskDescription'] = None
            else:
                transport_message_data['TaskDescription'] = int(task_description_value)

        # обработка списка пользователей
        message_body = transport_message_data['MessageBody']
        users_list = message_body['FullUserDataForClustering']
        for user in users_list:
            gender_value = user['gender']
            birthday_value = user['birthday']

            if gender_value is None or gender_value['@xsi:nil'] == 'true':
                user['gender'] = None
            if birthday_value is None or birthday_value['@xsi:nil'] == 'true':
                user['birthday'] = None
            if 'userPosts' not in user or user['userPosts'] is None:
                user['userPosts'] = []
            if 'userComments' not in user or user['userComments'] is None:
                user['userComments'] = []

        return TransportMessageWithBody(**transport_message_data)

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
            #msg_body: TransportMessageWithBody[List[FullUserDataForClustering]] = body.decode('utf-8')
            msg_body = body.decode('utf-8')
            result_object =  self.ParseXML(msg_body)

            return

        self.rmq_listener_channel.basic_consume(queue="CTQ", on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages')
        self.rmq_listener_channel.start_consuming()




