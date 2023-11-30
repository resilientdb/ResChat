import json
from channels.generic.websocket import AsyncWebsocketConsumer


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("call connect")
        with open("user_info.txt", "r") as f:
            my_name = f.read()
        friend_nickname = self.scope['url_route']['kwargs']['friend_nickname']
        if len(my_name) > len(friend_nickname):
            self.room_name = f'{my_name}-{friend_nickname}'
        else:
            self.room_name = f'{friend_nickname}-{my_name}'
        print("room:", self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
