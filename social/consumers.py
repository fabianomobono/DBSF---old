import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Friendship, User
import datetime

class ChatConsumer(WebsocketConsumer):
   
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['friendship_id']
        self.room_group_name = 'chat_%s' % self.room_name
        print(self.scope)
        print(self.room_group_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']
        friendship_id = self.scope['url_route']['kwargs']['friendship_id']
        message_to_save = Message(conversation=Friendship.objects.get(id=friendship_id), sender=User.objects.get(username=sender), receiver=User.objects.get(username=receiver), text=message, date_sent=datetime.datetime.now())
        message_to_save.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'receiver': receiver,
                'id': message_to_save.id,
                'date': message_to_save.date_sent.strftime("%a %b %d, %Y %H:%M:%S")
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        id = event['id']
        date = event['date']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'receiver': receiver,
            'id': id,
            'date': date,
        }))