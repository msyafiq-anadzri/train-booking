# middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class AuthMiddleware:
    """
    Middleware to ensure that all pages are protected from unauthenticated users.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path == reverse('bulk_upload'):
            return self.get_response(request)

        # Check if user is authenticated
        if not request.user.is_authenticated:
            # Redirect to login page unless the request is for login or signup
            if request.path not in [reverse('login'), reverse('register')]:
                return redirect('login')  # Adjust according to your login URL

        response = self.get_response(request)
        return response
