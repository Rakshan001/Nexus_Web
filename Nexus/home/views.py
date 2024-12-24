from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from alumni_details.models import Alumni, Student

# Home View (Open to everyone)
# def home(request):
#     if request.user.is_authenticated:
#         messages.success(request, f"Welcome back, {request.user.username}!")  # Display welcome message after login
#     return render(request, 'home/home.html')  # Publicly accessible home page

# @login_required
def home(request):
    first_name = ""
    last_name = ""
    email = ""

    if hasattr(request.user, 'alumni_profile'):  # Check if user is an alumni
        alumni = request.user.alumni_profile
        first_name = alumni.first_name
        last_name = alumni.last_name
        email = alumni.user.email
    elif hasattr(request.user, 'student_profile'):  # Check if user is a student
        student = request.user.student_profile
        first_name = student.first_name
        last_name = student.last_name
        email = student.email
    
    context = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email
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


from django.utils import timezone
from events_cec.models import Event

def home(request):
    now = timezone.now()
    current_date = now.date()
    current_time = now.time()

    # First, try to get an ongoing event
    ongoing_events = Event.objects.filter(
        date=current_date,
        time__lte=current_time
    ).order_by('time')[:1]

    # If no ongoing event, try to get an upcoming event
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

    events_to_display = []
    
    # First card priority logic
    if ongoing_events:
        # If there's an ongoing event, use it as first card
        events_to_display.extend(ongoing_events)
        # Then add up to 3 upcoming events, if available
        remaining_upcoming = upcoming_events[:3]
        events_to_display.extend(remaining_upcoming)
        # If still need more, add past events
        slots_remaining = 4 - len(events_to_display)
        if slots_remaining > 0:
            events_to_display.extend(past_events[:slots_remaining])
    
    elif upcoming_events:
        # If no ongoing but has upcoming, use first upcoming as first card
        first_upcoming = upcoming_events[:1]
        events_to_display.extend(first_upcoming)
        # Add up to 3 past events
        events_to_display.extend(past_events[:3])
    
    else:
        # If no ongoing or upcoming events, show 4 past events
        events_to_display.extend(past_events[:4])

    # Add current time context for template status display
    context = {
        'events': events_to_display,
        'current_date': current_date,
        'current_time': current_time,
    }
    
    return render(request, 'home/home.html', context)