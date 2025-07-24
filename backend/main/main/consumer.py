from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AdminNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("admin_notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("admin_notifications", self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))