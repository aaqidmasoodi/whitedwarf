from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async

# from accounts.models import User


class LiveLocationConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.user = self.scope["user"]
        print("User", self.user.name, "connected...")
        self.location_broadcast_id = self.get_location_broadcast_id(user)

        if self.location_broadcast_id:
            await self.channel_layer.group_add(
                self.location_broadcast_id,
                self.channel_name,
            )

        await self.send(
            {
                "type": "websocket.accept",
            }
        )

    @database_sync_to_async
    def get_location_broadcast_id(self, user):
        return "CUKBRS005"

    async def websocket_receive(self, event):
        print("Message Recieved")
        print(event["text"])

        if self.user.is_driver:
            print("sending to others...")
            await self.channel_layer.group_send(
                self.location_broadcast_id,
                {
                    "type": "live.location",
                    "message": event["text"],
                },
            )

    async def live_location(self, event):
        await self.send(
            {
                "type": "websocket.send",
                "text": event["message"],
            }
        )

    async def websocket_disconnect(self, event):
        print("DISCONNECTED.")
        await self.channel_layer.group_discard(
            self.location_broadcast_id,
            self.channel_name,
        )

        raise StopConsumer()
