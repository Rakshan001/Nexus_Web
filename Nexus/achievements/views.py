# # achievements/views.py

# from django.core.paginator import Paginator
# from django.shortcuts import render
# from .models import Achievement

# def achievements_list(request):
#     achievements = Achievement.objects.all().order_by('-date_achieved')  # Order by date achieved, for example
#     paginator = Paginator(achievements, 1)  # Show 10 achievements per page
#     page_number = request.GET.get('page')
#     achievements_page = paginator.get_page(page_number)

#     return render(request, 'achievements/achievements_list.html', {'achievements': achievements_page})



# *******************************

# achievements/views.py

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Achievement
from alumni_details.models import Alumni  # Import the Alumni model from your app

# View to display the list of achievements
def achievements_list(request):
    achievements = Achievement.objects.all().order_by('-date_achieved')  # Order by date achieved
    paginator = Paginator(achievements, 10)  # Show 10 achievements per page
    page_number = request.GET.get('page')
    achievements_page = paginator.get_page(page_number)

    return render(request, 'achievements/achievements_list.html', {'achievements': achievements_page})


# View to display the profile of an alumni
def alumni_profile(request, alumni_id):
    alumni = get_object_or_404(Alumni, pk=alumni_id)  # Fetch the alumni details using their ID
    return render(request, 'alumni_details/single-alumni-profile.html', {'alumni': alumni})
