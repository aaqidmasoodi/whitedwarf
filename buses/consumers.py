from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer


class LiveLocationConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        user = self.scope["user"]
        print("User", user.name, "connected...")
        await self.channel_layer.group_add(
            "test_group",
            self.channel_name,
        )

        await self.send(
            {
                "type": "websocket.accept",
            }
        )

    async def websocket_receive(self, event):
        print("Message Recieved")
        print(event["text"])
        user = self.scope["user"]

        if user.is_driver:
            print("sending to others...")
            await self.channel_layer.group_send(
                "test_group",
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
            "test_group",
            self.channel_name,
        )

        raise StopConsumer()