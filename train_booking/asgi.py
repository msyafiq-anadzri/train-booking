# train_booking/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import ticket_booking.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "train_booking.settings")
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            ticket_booking.routing.websocket_urlpatterns
        )
    ),
})
