import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Seat, Booking

class SeatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.train_id = self.scope['url_route']['kwargs']['train_id']
        self.room_group_name = f'booking_{self.train_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        seat_id = data['seat_id']
        action = data['action']

        seat = await self.lock_or_unlock_seat(seat_id, action)

        # Notify all users of the seat lock/unlock
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'seat_update',
                'seat_id': seat_id,
                'action': action,
                'is_locked': seat.is_locked,
                'is_booked': seat.is_booked,
            }
        )

    async def seat_update(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def lock_or_unlock_seat(self, seat_id, action):
        seat = Seat.objects.get(id=seat_id)
        if action == 'lock':
            seat.is_locked = True
        elif action == 'unlock':
            seat.is_locked = False
        seat.save()
        return seat
