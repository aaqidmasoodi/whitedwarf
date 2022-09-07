import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from core import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
core_asgi_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": core_asgi_application,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    routing.websocket_urlpatterns,
                )
            )
        ),
    }
)
