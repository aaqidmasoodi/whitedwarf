from django.urls import path
from buses import consumers

websocket_urlpatterns = [
    path(
        "api/buses/live/", consumers.LiveLocationConsumer.as_asgi(), name="socket-echo"
    ),
]
