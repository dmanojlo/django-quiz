from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
import json


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['url_route']['kwargs']['user']
        self.room_group_name = 'chat_%s' % self.room_name
        if self.user not in store.dummy_list:
            store.dummy_list.append(self.user)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'logged_users',
                'user': store.dummy_list,
            }
        )
    # async def tester_message(self, event):
    #     tester  = event['tester']
    #
    #     await self.send(text_data=json.dumps({'tester':tester,}))


    async def disconnect(self, close_code):

        self.user = self.scope['url_route']['kwargs']['user']
        store.dummy_list.remove(self.user)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'logged_users',
                'user': store.dummy_list,
            }
        )


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

         # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))
    # send logged users
    async def logged_users(self, event):
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'user': user,
        }))

#class to store logged users
class Usernames():

    def __init__(self):
        self.dummy_list = []

store = Usernames()
