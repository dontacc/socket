from channels.generic.websocket import WebsocketConsumer
import json


# all channels layer are asynchronous
from asgiref.sync import async_to_sync



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        

        # join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        print(self.room_name)
        print(self.channel_name)

        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)


    
    def receive(self, text_data):
        text_data = json.loads(text_data) # str to json
        message = text_data['message']


        # send message to room group
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {'type': 'chat_message',
                                                                            'message': message})
        

    def chat_message(self, data):
        message = data['message']

        # send message to websocket
        self.send(text_data=json.dumps({'message': message}))




class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()


    def disconnect(self, close_code):
        pass

    def receive(self, text):
        print(text)
        


