from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Origin(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Destination(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Train(models.Model):
    TRAIN_TYPES = [
        ('premium', 'Premium'),
        ('business', 'Business'),
        ('travel', 'Travel'),
        ('economy', 'Economy'),
    ]
    
    name = models.CharField(max_length=100)
    origin = models.ForeignKey('Origin', on_delete=models.CASCADE)
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])  # Price must be non-negative
    train_type = models.CharField(max_length=10, choices=TRAIN_TYPES)

    def __str__(self):
        return f"{self.name} ({self.get_train_type_display()})"

    def save(self, *args, **kwargs):
        if self.departure_time >= self.arrival_time:
            raise ValueError("Departure time must be before arrival time.")
        super().save(*args, **kwargs)

class Coach(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    coach_number = models.CharField(max_length=10)

class Seat(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    is_locked = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Example of additional field
    phone_number = models.CharField(max_length=15, blank=True)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=(('locked', 'Locked'), ('booked', 'Booked')))
    booked_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])  # Price must be non-negative

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])  # Payment must be non-negative
    payment_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
