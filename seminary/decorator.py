from django.contrib import messages
from django.shortcuts import redirect
from .models import Profile
from django.contrib.auth.decorators import user_passes_test

# Admin or Superuser access decorator
def admin_or_superuser_required(view_func):
    """
    Decorator that ensures the user is an admin or superuser.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            messages.error(request, "You must be an admin or superuser to access this page.")
            return redirect('home:home')  # Redirect to a relevant page (home or login)
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def verified_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Optional: you can redirect to login if the user isn't authenticated
            return redirect('login')  # Change this based on your login URL
        
        try:
            profile = Profile.objects.get(user=request.user)
            if not profile.is_verified:
                messages.error(request, "You need to be verified to access this page.")
                return redirect('seminary:request_membership')  # or another relevant page
        except Profile.DoesNotExist:
            messages.error(request, "Profile not found. Please create a profile first.")
            return redirect('seminary:request_membership')  # Handle the case where no profile is found

        return view_func(request, *args, **kwargs)

    return _wrapped_view
