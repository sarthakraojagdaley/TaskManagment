# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class TaskConsumer(AsyncWebsocketConsumer):
    group_name = "real_time_tasks"  # Update the group name here

    async def connect(self):
        await self.accept()

        # Add the user to the group when they connect
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

    async def disconnect(self, close_code):
        # Remove the user from the group when they disconnect
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def send_update(self, event):
        # This method will be called when a message with type 'send.update' is received
        # Implement the logic to send updates to the connected clients
        await self.send(text_data=event["data"])
