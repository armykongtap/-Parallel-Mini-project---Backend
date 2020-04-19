import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync

from user.models import User
from group.models import Group
from message.models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.room_group_name = 'chat_%s' % self.group_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': 'connected',
                'user_id': 0,
                # 'group_id': 0,
            }
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    # @sync_to_async
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']

        Message(msg_text=message, msg_sender=User.objects.get(
            pk=user_id), msg_group=Group.objects.get(pk=self.group_id)).save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
        }))
