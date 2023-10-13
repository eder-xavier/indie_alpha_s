import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.receiver_username = self.scope['url_route']['kwargs']['receiver']
        self.sender_username = self.scope['user'].username

        # Verifique se os usuários estão autorizados a conversar (você pode personalizar isso)
        if self.sender_username != self.receiver_username:
            await self.accept()
            await self.channel_layer.group_add(
                f'chat_{self.receiver_username}',
                self.channel_name
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f'chat_{self.receiver_username}',
            self.channel_name
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        # Enviar a mensagem para o cliente WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp,
        }))