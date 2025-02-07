from django.shortcuts import render,redirect
from .forms import ProfileForm, RoomAssignmentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorator import verified_only, admin_or_superuser_required
from .models import RoomAssignment, Profile


#After login or registeration the user can request to join the portals.
@login_required
def request_membership(request):
    # Check if the user already has a profile
    try:
        user_profile = Profile.objects.get(user=request.user)
        # If the user has a profile and it is pending
        if user_profile.is_verified is False:
            messages.info(request, "Your membership request is pending approval.")
            return redirect('home:home')  # Redirect to portal or home page

        # If the user already has an approved profile, prevent another request
        messages.error(request, "You have already been approved for membership.")
        return redirect('home:home')

    except Profile.DoesNotExist:
        # No profile exists, so allow them to submit a new request
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user  # Assign the current logged-in user
                profile.is_verified = False  # Initially set to False, as admin needs to verify
                profile.save()

                messages.success(request, "Your membership request has been submitted and is under review.")
                return redirect('home:home')  # Redirect after submission
            else:
                messages.error(request, "There was an error with your submission. Please try again.")
        else:
            form = ProfileForm()

        canonical_url = request.build_absolute_uri(request.path)

        return render(request, 'seminary/request_membership.html', {'canonical_url': canonical_url, 'form': form})

# seminary portal verification

@login_required
def seminary_portal(request):
    return render(request, 'seminary/seminary_portal.html')

# views.py
@login_required
@verified_only
@admin_or_superuser_required
def assign_room(request):
    if request.method == 'POST':
        form = RoomAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Room successfully assigned!")
            return redirect('seminary:room_details')  # Redirect to the rooms page or another relevant page
    else:
        form = RoomAssignmentForm()

    return render(request, 'seminary/assign_room.html', {'form': form})


# list of the rooms
@login_required
@verified_only
def room_details(request):
    rooms = RoomAssignment.objects.all()
    canonical_url = request.build_absolute_uri(request.path)
    context = {'canonical_url':canonical_url, 'rooms': rooms}
    return render (request, 'seminary/room_details.html', context)
    