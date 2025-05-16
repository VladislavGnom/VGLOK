import json
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from mainapp.models import Chat, Message


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.user = self.scope['user']
        self.room_group_name = f'personal_chat_{self.chat_id}'

        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        if not await self.is_valid_chat():
            await self.close()
            return
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        history = await self.get_chat_history()
        for msg in history:
            await self.send(text_data=json.dumps({
                'message': msg.text,
                'sender_id': msg.sender_id,
                'timestamp': msg.timestamp.isoformat(),
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        saved_message = await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.user.id,
                'timestamp': saved_message.timestamp.isoformat(),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'timestamp': event['timestamp'],
        }))

    @sync_to_async
    def is_valid_chat(self):
        '''Check that the chat is already exist and the user is member into it'''
        return Chat.objects.filter(
            Q(user1=self.user) | Q(user2=self.user),
            id=self.chat_id,
        ).exists()

    @sync_to_async
    def save_message(self, text):
        '''Save the message in DB'''
        chat = Chat.objects.get(id=self.chat_id)
        return Message.objects.create(
            chat=chat,
            sender=self.user,
            text=text,
        )
    
    @sync_to_async
    def get_chat_history(self):
        return list(Message.objects.filter(chat_id=self.chat_id).order_by('-timestamp')[:50])
