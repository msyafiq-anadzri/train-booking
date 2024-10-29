# ticket_booking/admin.py
from django.contrib import admin
from .models import *


admin.site.register(Train)
admin.site.register(Coach)
admin.site.register(Seat)
admin.site.register(Origin)
admin.site.register(Destination)
admin.site.register(Booking)
admin.site.register(Payment)
