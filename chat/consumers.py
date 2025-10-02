import json 
from channels.generic.websocket import AsyncWebsocketConsumer

connected_users = {}

# REDIS_URL = 'redis://127.0.0.1:6379'

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["pk"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]


        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # #track user in redis
        # self.redis = await aioredis.from_url(REDIS_URL, decode_response=True)
        # await self.redis.sadd(f"chatroom:{self.room_name}:users", self.user.username)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # #romove from redis
        # await self.redis.srem(f"chatroom:{self.room_name}:users", self.user.username)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        ms = data["message"]
        username = self.scope['user'].username
        # users = await self.redis.smembers(f"chatroom:{self.room_name}:users")
       
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", 
                                   "message": ms,
                                   "username": username,
                                #    "users": list(users),
                                   })

    # Receive message from room group
    async def chat_message(self, event):
        ms = event["message"]
        user = event["username"]

        if user == self.scope["user"].username:
            is_from_me = True
        else:
            is_from_me = False
        await self.send(text_data=json.dumps({"message": ms,
                                              "username": user,
                                              "is_from_me": is_from_me,
                                              }))