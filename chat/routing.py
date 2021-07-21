from django.urls import re_path
from . import consumers
websocket_url_patterns = [
        re_path(r'wss/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
]
