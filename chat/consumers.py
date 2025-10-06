import json 
from channels.generic.websocket import AsyncWebsocketConsumer

conn_users = {}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["pk"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]


        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        conn_users.setdefault(self.room_name, set()).add(self.user.username)
        await self.accept()

        #send list
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "user_list",
                                   "users": list(conn_users[self.room_name])}
        )

    async def disconnect(self, close_code):
        #clean list when user leaves
        if self.room_name in conn_users:
            conn_users[self.room_name].discard(self.user.username)

            #send new list updated
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "user_list",
                                       "users": list(conn_users[self.room_name])}
            )

        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

     

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        ms = data["message"]
        username = self.scope['user'].username
       
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", 
                                   "message": ms,
                                   "username": username,
                                   })

    # Receive message from room group
    async def chat_message(self, event):
        ms = event["message"]
        user = event["username"]

        if user == self.scope["user"].username:
            is_from_me = True
        else:
            is_from_me = False
        await self.send(text_data=json.dumps({"type":"chat",
                                              "message": ms,
                                              "username": user,
                                              "is_from_me": is_from_me,
                                              }))
    async def user_list(self, event):
        await self.send(text_data=json.dumps({
            "type": "users",
            "users": event["users"],
        }))