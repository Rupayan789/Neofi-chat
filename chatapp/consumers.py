
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth import get_user_model, authenticate
from .models.message import Message
from asgiref.sync import sync_to_async

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    
    async def connect(self):
        print("Websocket connection")
        my_id = self.scope['user'].user_id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # leave group room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json['text']
        sender_id = self.scope['user'].user_id
        receiver_id = self.scope['url_route']['kwargs']['id']

        await self.save_message(sender_id=sender_id,room_name=self.room_name,text=text)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chatbox_message",
                "text": text,
                "sender_id": sender_id,
                "receiver_id": receiver_id,
            },
        )
    async def chatbox_message(self, event):
        text = event["text"]
        sender_id = event["sender_id"]
        receiver_id = event["receiver_id"]
        
        await self.send(
            text_data=json.dumps(
                {
                    "text": text,
                    "sender_id": sender_id,
                    "receiver_id": receiver_id,
                    
                }
            )
        )
    @sync_to_async
    def save_message(self,sender_id,room_name,text):
        user = User.objects.get(user_id=sender_id)
        Message.objects.create(author=user,room_name=room_name,content=text)



    