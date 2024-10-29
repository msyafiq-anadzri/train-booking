# ticket_booking/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from .forms import *
from .models import Train, Coach, Seat, Booking, Payment, Origin, Destination


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'ticket_booking/register.html', {'form': form})


def profile(request):
    return render(request, 'ticket_booking/profile.html')


def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'ticket_booking/edit_profile.html', {'form': form})









from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q  # Import Count and Q for conditional aggregation
from .models import Train
from .forms import TrainSearchForm

def home(request):
    form = TrainSearchForm()
    trains = None  # Initialize trains to None for context

    # Check if the request is POST for search
    if request.method == 'POST':
        form = TrainSearchForm(request.POST)
        if form.is_valid():
            train_type = form.cleaned_data.get('train_type')
            origin_id = form.cleaned_data.get('origin')
            destination_id = form.cleaned_data.get('destination')
            departure_date = form.cleaned_data.get('departure_date')
            return_date = form.cleaned_data.get('return_date')

            # Query to find trains based on input criteria
            trains = Train.objects.filter(
                origin_id=origin_id,
                destination_id=destination_id,
                departure_time__date=departure_date,
                train_type=train_type,
                departure_time__gt=timezone.now()  # Only show future trains
            )

            if not trains.exists():
                messages.info(request, "No trains available for the selected criteria.")
            else:
                return redirect('train_info', train_id=trains.first().id)  # Redirect to train_info with the first train's ID

    # Fetch all future trains with available seats
    trains = Train.objects.filter(departure_time__gt=timezone.now()).annotate(
        available_seats=Count('coach__seat', filter=Q(coach__seat__is_booked=False))
    )

    return render(request, 'ticket_booking/home.html', {'form': form, 'trains': trains})




def train_info(request, train_id):
    train = get_object_or_404(Train, id=train_id)
    
    # Get all coaches for the train
    coaches = Coach.objects.filter(train=train)
    
    # Calculate total available seats by counting unbooked seats in all coaches of this train
    total_available_seats = Seat.objects.filter(coach__in=coaches, is_booked=False).count()
    
    # Total number of coaches
    total_coaches = coaches.count()

    return render(request, 'ticket_booking/train_info.html', {
        'train': train,
        'coaches': coaches,
        'total_coaches': total_coaches,
        'total_available_seats': total_available_seats,
    })


def select_train(request, train_id):
    train = get_object_or_404(Train, id=train_id)
    coaches = Coach.objects.filter(train=train)

    # Calculate available seats for each coach
    for coach in coaches:
        coach.available_seats = coach.seat_set.filter(is_booked=False).count()

    return render(request, 'ticket_booking/select_coach.html', {'train': train, 'coaches': coaches})




def select_coach(request, coach_id):
    coach = get_object_or_404(Coach, id=coach_id)
    seats = Seat.objects.filter(coach=coach, is_booked=False)
    return render(request, 'ticket_booking/select_coach.html', {'coach': coach, 'seats': seats})


def select_seat(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)
    if request.method == 'POST':
        seat.is_locked = True
        seat.save()
        booking = Booking.objects.create(user=request.user, seat=seat, status='locked', total_amount=100.00)  # Placeholder for amount
        return redirect('booking_summary', booking_id=booking.id)
    return render(request, 'ticket_booking/select_seat.html', {'seat': seat})


def booking_summary(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'ticket_booking/booking_summary.html', {'booking': booking})


def confirm_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        Payment.objects.create(booking=booking, amount=booking.total_amount, is_paid=True)
        booking.status = 'booked'
        booking.seat.is_booked = True
        booking.seat.is_locked = False
        booking.seat.save()
        booking.save()
        return redirect('booking_confirmation', booking_id=booking.id)
    return render(request, 'ticket_booking/confirm_payment.html', {'booking': booking})


def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'ticket_booking/booking_confirmation.html', {'booking': booking})
