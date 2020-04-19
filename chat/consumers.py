import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from channels.layers import get_channel_layer

from user.models import User
from group.models import Group
from message.models import Message


class ChatConsumer(WebsocketConsumer):
    def message_to_dict(self, m):
        return({
            'type': 'chat_message',
            'msg_text': m.msg_text,
            'user_name': m.msg_sender.user_name,
            'time_stamp': m.msg_timestamp.timestamp()
        })

    # -------------------------------------------------------------

    def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.room_group_name = 'chat_%s' % self.group_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        # intMessage = Message.objects.filter(msg_group_id=self.group_id)
        # if (Message.objects.count() >= 100):
        #     n = Message.objects.count()-100
        # else:
        #     n = 0
        # for m in intMessage[n:]:
        #     async_to_sync(self.channel_layer.group_send)(
        #         self.room_group_name, self.message_to_dict(m))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg_text = text_data_json['msg_text']
        user_name = text_data_json['user_name']

        m = Message(msg_text=msg_text, msg_sender=User.objects.get(
            user_name=user_name), msg_group=Group.objects.get(pk=self.group_id))
        m.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, self.message_to_dict(m))
    # Receive message from room group

    def chat_message(self, event):
        msg_text = event['msg_text']
        user_name = event['user_name']
        time_stamp = event['time_stamp']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'msg_text': msg_text,
            'user_name': user_name,
            'time_stamp': time_stamp,
        }))
