# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from app.consumers import TaskConsumer

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/websock/", TaskConsumer.as_asgi()),
                ]
            )
        ),
    }
)

channel_routing = {
    "websocket.connect": TaskConsumer.connect,
    "websocket.disconnect": TaskConsumer.disconnect,
    "send.update": TaskConsumer.send_update,
}
