# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit.")
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in password):
            raise ValidationError("Password must contain at least one special character.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        

from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken.")
        return email



# ticket_booking/forms.py
from django import forms
from .models import Origin, Destination, Train

class TrainSearchForm(forms.Form):
    TRAIN_TYPES = Train.TRAIN_TYPES

    train_type = forms.ChoiceField(choices=TRAIN_TYPES, required=True)
    origin = forms.ModelChoiceField(queryset=Origin.objects.all(), required=True)
    destination = forms.ModelChoiceField(queryset=Destination.objects.all(), required=True)
    departure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    return_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    pax = forms.IntegerField(min_value=1, required=True)
