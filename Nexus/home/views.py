from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from alumni_details.models import Alumni, Student
from django.utils import timezone
from events_cec.models import Event

# Home View (Open to everyone)
# def home(request):
#     if request.user.is_authenticated:
#         messages.success(request, f"Welcome back, {request.user.username}!")  # Display welcome message after login
#     return render(request, 'home/home.html')  # Publicly accessible home page

# @login_required
def home(request):
    # Get user details
    first_name = ""
    last_name = ""
    email = ""

    if request.user.is_authenticated:
        if hasattr(request.user, 'alumni_profile'):
            alumni = request.user.alumni_profile
            first_name = alumni.first_name
            last_name = alumni.last_name
            email = alumni.user.email
        elif hasattr(request.user, 'student_profile'):
            student = request.user.student_profile
            first_name = student.first_name
            last_name = student.last_name
            email = student.email

    # Get events
    now = timezone.now()
    current_date = now.date()
    current_time = now.time()

    # Get ongoing events
    ongoing_events = Event.objects.filter(
        date=current_date,
        time__lte=current_time
    ).order_by('time')

    # Get upcoming events (including today's future events)
    upcoming_events = Event.objects.filter(
        date__gte=current_date
    ).exclude(
        date=current_date,
        time__lte=current_time
    ).order_by('date', 'time')

    # Get past events
    past_events = Event.objects.filter(
        date__lt=current_date
    ).order_by('-date', '-time')

    # Debug prints
    print("Ongoing events:", ongoing_events.count())
    print("Upcoming events:", upcoming_events.count())
    print("Past events:", past_events.count())

    # Combine events with priority
    events_to_display = []
    
    # Add ongoing events (up to 2)
    events_to_display.extend(ongoing_events[:2])
    
    # Add upcoming events (up to 4 total)
    remaining_slots = 4 - len(events_to_display)
    if remaining_slots > 0:
        events_to_display.extend(upcoming_events[:remaining_slots])
    
    # Add past events if needed
    remaining_slots = 4 - len(events_to_display)
    if remaining_slots > 0:
        events_to_display.extend(past_events[:remaining_slots])

    context = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'events': events_to_display,
        'current_date': current_date,
        'current_time': current_time,
    }
    
    return render(request, 'home/home.html', context)



# User Login View (Simplified)
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Login successful. Welcome, {user.username}!")
            return redirect('home')  # Redirect to home page after successful login
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'home/login.html')  # Render the login page if not logged in

# Logout View
@login_required
def user_logout(request):
    list(messages.get_messages(request))
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')  # Redirect to home page after logout

# Alumni Profile View (Login and Alumni Check Required)
@login_required
def alumni_profile(request):
    list(messages.get_messages(request))
    try:
        alumni = Alumni.objects.get(user=request.user, is_alumni=True)  # Check if the user is an alumni
    except Alumni.DoesNotExist:
        messages.error(request, "You are not authorized to view this page as you're not an alumni.")
        return redirect('home')  # Redirect non-alumni users to home page
    return render(request, 'alumni_details/update-alumni-profile.html', {'alumni': alumni})  # Alumni profile view


def nexusTeam(request):
    return render(request, 'home/nexusTeam.html')

def webTeam(request):
    return render(request, 'home/webTeam.html')




