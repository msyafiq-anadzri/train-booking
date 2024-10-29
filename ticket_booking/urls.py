# ticket_booking/urls.py
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('train-info/<int:train_id>/', views.train_info, name='train_info'),


    path('train/<int:train_id>/', views.train_info, name='train_info'),
    path('select/train/<int:train_id>/', views.select_train, name='select_train'),
    path('select/coach/<int:coach_id>/', views.select_coach, name='select_coach'),
    path('seat/<int:seat_id>/', views.select_seat, name='select_seat'),
    path('booking/summary/<int:booking_id>/', views.booking_summary, name='booking_summary'),
    path('payment/confirm/<int:booking_id>/', views.confirm_payment, name='confirm_payment'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
]
