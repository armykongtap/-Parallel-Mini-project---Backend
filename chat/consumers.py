import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from channels.layers import get_channel_layer
from pytz import timezone

from user.models import User
from group.models import Group
from message.models import Message


class ChatConsumer(WebsocketConsumer):
    online_user = set()

    def message_to_dict(self, m):
        return({
            'type': 'chat_message',
            'msg_id': m.msg_id,
            'msg_text': m.msg_text,
            'user_name': m.msg_sender.user_name,
            'time_stamp': timezone('Asia/Bangkok').localize(m.msg_timestamp).strftime("%H:%M")
        })

    def update_recent_message(self, msg_id):
        user = User.objects.get(user_name=self.user_name)
        newmsg = Message.objects.get(msg_id=msg_id)
        getmsg = user.user_recent_message.filter(msg_group=self.group_id)
        if newmsg.msg_group.group_id == self.group_id:
            if getmsg.exists():
                rm = user.user_recent_message.get(msg_group=self.group_id)
                if msg_id > rm.msg_id:
                    user.user_recent_message.remove(rm)
                    user.user_recent_message.add(newmsg)
            else:
                user.user_recent_message.add(newmsg)

    def get_recent_message(self):
        query = {}
        query['user_name'] = self.user_name
        query['group_id'] = self.group_id
        getmsg = User.objects.get(
            user_name=self.user_name).user_recent_message.filter(msg_group=self.group_id)
        if getmsg.exists():
            query['recent_msg_id'] = getmsg[0].msg_id
        else:
            query['recent_msg_id'] = 0
        return query

    # -------------------------------------------------------------

    def connect(self):
        self.group_id = int(self.scope['url_route']['kwargs']['group_id'])
        self.room_group_name = 'chat_%s' % self.group_id
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.online_user.add(self.user_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        self.send(text_data=json.dumps(
            self.get_recent_message()))

        initMessage = Message.objects.filter(msg_group_id=self.group_id)
        if (initMessage.count() > 10):
            n = initMessage.count()-10
        else:
            n = 0
        for m in initMessage[n:]:
            self.send(text_data=json.dumps(self.message_to_dict(m)))
        if initMessage.count() > 0:
            self.update_recent_message(
                initMessage[initMessage.count()-1].msg_id)

    def disconnect(self, close_code):
        self.online_user.discard(
            self.user_name)
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        msg_text = text_data_json['msg_text']

        m = Message(msg_text=msg_text, msg_sender=User.objects.get(
            user_name=self.user_name), msg_group=Group.objects.get(pk=self.group_id))
        m.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, self.message_to_dict(m))

    # Receive message from room group
    def chat_message(self, event):
        msg_id = event['msg_id']
        msg_text = event['msg_text']
        user_name = event['user_name']
        time_stamp = event['time_stamp']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'msg_id': msg_id,
            'msg_text': msg_text,
            'user_name': user_name,
            'time_stamp': time_stamp,
        }))

        self.update_recent_message(msg_id)
