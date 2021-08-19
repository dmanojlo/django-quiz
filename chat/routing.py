from django.urls import re_path
from . import consumers
websocket_url_patterns = [
        re_path(r'ws/chat/(?P<room_name>\w+)/(?P<user>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
]
