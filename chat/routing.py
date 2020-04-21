from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/user_name=(?P<user_name>\w+)&group_id=(?P<group_id>\w+)/$',
            consumers.ChatConsumer),
]
