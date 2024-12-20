import string
from typing import List
import pika
import xmltodict
from pika.exceptions import ChannelWrongStateError, StreamLostError, AMQPConnectionError
from BusinessLogic.TransportModels.full_user_data_for_clustering import FullUserDataForClustering
from BusinessLogic.TransportModels.transport_message import TransportMessage
from BusinessLogic.TransportModels.transport_message_with_body import TransportMessageWithBody


class DataExtractor:
    rmq_conn_str: string = "localhost"
    rmq_params: pika.ConnectionParameters
    rmq_listener_connection: pika.BlockingConnection
    queue_state = None
    result_list: List[FullUserDataForClustering] = []


    def __init__(self):
        self.rmq_params = pika.ConnectionParameters(self.rmq_conn_str)
        self.rmq_listener_connection = pika.BlockingConnection(self.rmq_params)
        self.rmq_listener_channel = self.rmq_listener_connection.channel()
        self.queue_state = self.rmq_listener_channel.queue_declare("CTQ", durable=True, exclusive=False, auto_delete=False)

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

            if gender_value is None or (isinstance(gender_value, dict) and gender_value['@xsi:nil'] == 'true'):
                user['gender'] = None
            if birthday_value is None or (isinstance(birthday_value, dict) and birthday_value['@xsi:nil'] == 'true'):
                user['birthday'] = None
            if 'userPosts' not in user or user['userPosts'] is None:
                user['userPosts'] = []
            if 'userComments' not in user or user['userComments'] is None:
                user['userComments'] = []

        return TransportMessageWithBody(**transport_message_data)

    # базовый метод публикации сообщения в реббит
    def basic_publish(self):
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

    # базовый метод получения данных по реббит
    def basic_consume(self):
        q_length = self.queue_state.method.message_count
        all_messages_received = False
        if not q_length:
            print("Очередь сообщений пуста!")
            return

        try:
            for method_frame, properties, body in self.rmq_listener_channel.consume("CTQ"):
                try:
                    all_messages_received = self._process_message(body)
                except:
                    print(f"Rabbit Consumer : Received message in wrong format {str(body)}")

                self.rmq_listener_channel.basic_ack(method_frame.delivery_tag)

                if method_frame.delivery_tag == q_length or all_messages_received:
                    break

        except (ChannelWrongStateError, StreamLostError, AMQPConnectionError) as e:
            print(f'Connection Interrupted: {str(e)}')
        finally:
            self.rmq_listener_channel.close()
            self.rmq_listener_connection.close()


    #метод обработки сообщения
    def _process_message(self, body) -> bool:
        if body is None:
            print("Failed to retrieve user data!")
        msg_body = body.decode('utf-8')
        result_object = self.ParseXML(msg_body)
        # globals()["users_list"] = result_object.MessageBody
        self.result_list.append(result_object.MessageBody)
        return  result_object.IsLastChunk

