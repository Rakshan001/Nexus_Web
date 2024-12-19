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


