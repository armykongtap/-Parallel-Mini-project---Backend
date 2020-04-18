import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from rest_framework.parsers import JSONParser

from user.models import User
from group.models import Group
from message.models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    @sync_to_async
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg = text_data_json['msg']
        group_id = text_data_json['group_id']
        user_id = text_data_json['user_id']

        Message(msg_text=msg, msg_sender=User.objects.get(
            pk=user_id), msg_group=Group.objects.get(pk=group_id)).save()

        # Send message to room group
        text_data_json['type'] = 'chat_message'
        self.channel_layer.group_send(self.room_group_name, text_data_json)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
