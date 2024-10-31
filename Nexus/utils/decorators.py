# utils/decorators.py

from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def login_required_with_message(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'Please log in first to access this page.')
            return redirect('user_login')  # Use your actual app name for the login URL
        return view_func(request, *args, **kwargs)
    return _wrapped_view
