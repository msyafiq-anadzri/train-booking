from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/booking/<int:train_id>/', consumers.SeatConsumer.as_asgi()),
]
