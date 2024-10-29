# train_booking/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from ticket_booking.views import *
from ticket_booking.views_api import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('register/', register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='ticket_booking/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/edit/', edit_profile, name='edit_profile'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='ticket_booking/password_reset.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='ticket_booking/password_reset_done.html'), name='password_reset_done'),
    path('', include('ticket_booking.urls')),  # include the app's URLs
    path('api/bulk-upload/', bulk_upload, name='bulk_upload'),
]
