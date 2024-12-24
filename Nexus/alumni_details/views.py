# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Alumni
from .forms import AlumniUpdateForm
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.contrib import messages
from utils.decorators import login_required_with_message  # Import the decorator
from notifications.utils import create_profile_view_notification





@login_required_with_message
def alumni_profile(request):
    list(messages.get_messages(request))
    # Fetch the alumni object
    alumni = get_object_or_404(Alumni, user=request.user)
    
    # Check if the user is an alumni
    if not alumni.is_alumni:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('home')
    
    # Fetch all memories for the alumni
    memories = alumni.memories.all()

    # Render the alumni profile page with alumni and memories
    return render(request, 'alumni_details/alumni-profile.html', {'alumni': alumni, 'memories': memories})




@login_required_with_message
def update_alumni_profile(request):
    list(messages.get_messages(request))
    alumni = get_object_or_404(Alumni, user=request.user)

    if not alumni.is_alumni:
        messages.error(request, "You are not authorized to update this profile.")
        return redirect('home')

    # Get the path of the old image before updating
    old_image_path = alumni.profile_picture.path if alumni.profile_picture else None

    if request.method == 'POST':
        form = AlumniUpdateForm(request.POST, request.FILES, instance=alumni)

        if form.is_valid():
            # Save the form first
            form.save()

            # If a new profile picture is uploaded, remove the old one from the file system
            if request.FILES.get('profile_picture') and old_image_path:
                if os.path.exists(old_image_path) and old_image_path != 'photos/default.png':  # Avoid removing the default image
                    os.remove(old_image_path)

            messages.success(request, "Your profile has been updated successfully!")
            return redirect('alumni_profile')
    else:
        form = AlumniUpdateForm(instance=alumni)
        memories = alumni.memories.all()

    return render(request, 'alumni_details/update-alumni-profile.html', {'form': form, 'alumni': alumni ,'memories': memories})


'''Deleting profile picture'''
@login_required
def delete_profile_picture(request):
    alumni = get_object_or_404(Alumni, user=request.user)

    if not alumni.is_alumni:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('home')

    # Check if the alumni has a profile picture to delete
    if alumni.profile_picture and alumni.profile_picture != 'photos/default.png':  # Avoid deleting the default image
        # Remove the file from the filesystem
        if os.path.exists(alumni.profile_picture.path):
            os.remove(alumni.profile_picture.path)
        # Clear the profile_picture field
        alumni.profile_picture = None
        alumni.save()
        messages.success(request, "Profile picture has been deleted successfully!")
    else:
        messages.error(request, "No profile picture to delete.")

    return redirect('update_alumni_profile')


''''==========================='''
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Alumni, AlumniMemory
import os
from django.conf import settings

@login_required
def manage_memories(request):
    alumni = get_object_or_404(Alumni, user=request.user)

    if not alumni.is_alumni:
        return JsonResponse({'error': 'You are not authorized to manage memories.'}, status=403)

    if request.method == 'POST':
        if alumni.memories.count() >= 5:
            return JsonResponse({'error': 'You can upload up to 5 images only.'}, status=400)

        image = request.FILES.get('image')
        if not image:
            return JsonResponse({'error': 'No image uploaded.'}, status=400)

        # Save the image as a new memory
        memory = AlumniMemory.objects.create(alumni=alumni, image=image)
        return JsonResponse({
            'message': 'Image uploaded successfully.',
            'image_url': memory.image.url,
            'memory_id': memory.id
        }, status=201)

    elif request.method == 'DELETE':
        memory_id = request.GET.get('memory_id')
        memory = get_object_or_404(AlumniMemory, id=memory_id, alumni=alumni)

        # Delete the file and database entry
        if os.path.exists(memory.image.path):
            os.remove(memory.image.path)
        memory.delete()

        return JsonResponse({'message': 'Image deleted successfully.'}, status=200)

    # Render the template with existing memories
    memories = alumni.memories.all()
    return render(request, 'alumni_details/alumni-profile/alumni-memory.html', {'alumni': alumni, 'memories': memories})




# *****************************



# from django.shortcuts import render, get_object_or_404
# from .models import Alumni
# import datetime
# @login_required_with_message
# def alumni_list(request):
#     current_year = datetime.datetime.now().year
#     graduation_years = Alumni.objects.values_list('graduation_year', flat=True).distinct().order_by('-graduation_year')

#     # Get alumni for the current year sorted alphabetically
#     alumni_current_year = Alumni.objects.filter(graduation_year=current_year).order_by('first_name')[:5]

#     # Get alumni for previous years sorted alphabetically
#     alumni_previous_years = {}
#     for year in graduation_years:
#         if year < current_year:
#             alumni_previous_years[year] = Alumni.objects.filter(graduation_year=year).order_by('first_name')[:5]


#     return render(request, 'alumni_details/alumni_list.html', {
#         'current_year': current_year,
#         'alumni_current_year': alumni_current_year,
#         'alumni_previous_years': alumni_previous_years,
#         'graduation_years': graduation_years,
#     })
# views.py
# views.py
from django.http import JsonResponse

@login_required_with_message
def alumni_list(request):
    # Get all distinct graduation years ordered by most recent first
    graduation_years = Alumni.objects.values_list('graduation_year', flat=True).distinct().order_by('-graduation_year')
    
    # Initial number of years to show
    initial_years = 2
    
    # Get the years to display initially
    visible_years = graduation_years[:initial_years]
    
    # Create a dictionary to store alumni by year
    alumni_by_year = {}
    
    # Populate the dictionary with alumni for each visible year
    for year in visible_years:
        alumni_by_year[year] = Alumni.objects.filter(graduation_year=year).order_by('first_name')[:5]
    
    return render(request, 'alumni_details/alumni_list.html', {
        'alumni_by_year': alumni_by_year,
        'graduation_years': graduation_years,
        'current_year': graduation_years[0] if graduation_years else None,
        'has_more': len(graduation_years) > initial_years,
        'next_page': initial_years,
    })

@login_required_with_message
def load_more_years(request):
    page = int(request.GET.get('page', 0))
    years_per_load = 2  # Number of additional years to load
    
    # Get all graduation years
    graduation_years = Alumni.objects.values_list('graduation_year', flat=True).distinct().order_by('-graduation_year')
    
    # Calculate the range for the next batch of years
    start_idx = page
    end_idx = page + years_per_load
    
    # Get the next batch of years
    next_years = graduation_years[start_idx:end_idx]
    
    # Prepare the data for the response
    data = {}
    for year in next_years:
        alumni_list = Alumni.objects.filter(graduation_year=year).order_by('first_name')[:5]
        data[year] = [{
            'id': alumni.alumni_id,
            'first_name': alumni.first_name,
            'last_name': alumni.last_name,
            'current_position': alumni.current_position,
            'company_name': alumni.company_name,
            'linkedin_url': alumni.linkedin_url,
            'profile_picture': alumni.profile_picture.url if alumni.profile_picture else None,
        } for alumni in alumni_list]
    
    return JsonResponse({
        'years': data,
        'has_more': end_idx < len(graduation_years),
        'next_page': end_idx
    })


'''Below code with paginator'''
# from django.core.paginator import Paginator
# from django.shortcuts import render, redirect
# from .models import Alumni

# @login_required_with_message
# def alumni_by_year(request, graduation_year):
#     # Fetch all distinct branches for the filter dropdown
#     branches = Alumni.objects.values_list('branch', flat=True).distinct()

#     # Get the selected branch from the GET parameters (if any)
#     selected_branch = request.GET.get('branch', '')

#     # If a filter is applied, adjust the alumni queryset
#     # alumni = Alumni.objects.filter(graduation_year=graduation_year)
#     alumni = Alumni.objects.filter(graduation_year=graduation_year).order_by('first_name')  # Alphabetical order

#     if selected_branch:
#         alumni = alumni.filter(branch=selected_branch)

#     # Pagination logic
#     page = request.GET.get('page', 1)  # Default to page 1
#     paginator = Paginator(alumni, 5)  # Show 5 alumni profiles per page
#     try:
#         alumni_page = paginator.page(page)
#     except:
#         alumni_page = paginator.page(1)  # In case of an invalid page number

#     # Fetch all distinct graduation years for the filter dropdown
#     graduation_years = Alumni.objects.values_list('graduation_year', flat=True).distinct()

#     return render(request, 'alumni_details/alumni_by_year.html', {
#         'alumni': alumni_page,  # Send the paginated alumni profiles
#         'current_year': graduation_year,
#         'graduation_year': graduation_year,
#         'graduation_years': graduation_years,
#         'branches': branches,  # For the branch filter dropdown
#         'selected_branch': selected_branch,  # To keep track of the selected branch
#         'paginator': paginator,  # Pass the paginator object for future navigation
#     })

'''```````````````````````'''
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Alumni

@login_required_with_message
def alumni_by_year(request, graduation_year):
    # Fetch all distinct branches for the filter dropdown
    branches = Alumni.objects.values_list('branch', flat=True).distinct()

    # Get the selected branch from the GET parameters (if any)
    selected_branch = request.GET.get('branch', '')

    # Check if the filter form was submitted for graduation year
    if 'graduation_year' in request.GET and request.GET['graduation_year']:
        graduation_year = int(request.GET.get('graduation_year'))
        return redirect('alumni_by_year', graduation_year=graduation_year)

    # If graduation_year is provided in the URL, fetch alumni for that year
    alumni = Alumni.objects.filter(graduation_year=graduation_year).order_by('first_name')  # Alphabetical order

    # If a branch is selected, filter the alumni based on the selected branch
    if selected_branch:
        alumni = alumni.filter(branch=selected_branch)

    # Pagination logic
    page = request.GET.get('page', 1)  # Default to page 1
    paginator = Paginator(alumni, 5)  # Show 5 alumni profiles per page
    try:
        alumni_page = paginator.page(page)
    except:
        alumni_page = paginator.page(1)  # In case of an invalid page number

    # Fetch all distinct graduation years for the filter dropdown
    graduation_years = Alumni.objects.values_list('graduation_year', flat=True).distinct()

    return render(request, 'alumni_details/alumni_by_year.html', {
        'alumni': alumni_page,  # Send the paginated alumni profiles
        'current_year': graduation_year,
        'graduation_year': graduation_year,
        'graduation_years': graduation_years,
        'branches': branches,  # For the branch filter dropdown
        'selected_branch': selected_branch,  # To keep track of the selected branch
        'paginator': paginator,  # Pass the paginator object for future navigation
    })



''' above code with pagination'''




# from django.shortcuts import render, redirect
# from .models import Alumni

# @login_required_with_message
# def alumni_by_year(request, graduation_year):
#     # Fetch all distinct branches for the filter dropdown
#     branches = Alumni.objects.values_list('branch', flat=True).distinct()

#     # Get the selected branch from the GET parameters (if any)
#     selected_branch = request.GET.get('branch', '')

#     # Check if the filter form was submitted for graduation year
#     if 'graduation_year' in request.GET and request.GET['graduation_year']:
#         graduation_year = int(request.GET.get('graduation_year'))
#         return redirect('alumni_by_year', graduation_year=graduation_year)

#     # If graduation_year is provided in the URL, fetch alumni for that year
#     alumni = Alumni.objects.filter(graduation_year=graduation_year)

#     # If a branch is selected, filter the alumni based on the selected branch
#     if selected_branch:
#         alumni = alumni.filter(branch=selected_branch)

#     # Fetch all distinct graduation years for the filter dropdown
#     graduation_years = Alumni.objects.values_list('graduation_year', flat=True).distinct()

#     return render(request, 'alumni_details/alumni_by_year.html', {
#         'alumni': alumni,
#         'current_year': graduation_year,
#         'graduation_year': graduation_year,
#         'graduation_years': graduation_years,
#         'branches': branches,  # For the branch filter dropdown
#         'selected_branch': selected_branch,  # To keep track of the selected branch
#     })



# '''




'''' Alumni-Profile'''
# from notifications.utils import create_profile_view_notification
# @login_required_with_message
# def public_alumni_profile(request, alumni_id):
#     alumni = get_object_or_404(Alumni, pk=alumni_id)
    
#     # Create notification only if viewer is not the profile owner
#     if request.user != alumni.user:
#         create_profile_view_notification(request.user, alumni.user)
    
#     return render(request, 'alumni_details/alumni-profile/public-alumni-profile.html', {'alumni': alumni})

@login_required_with_message
def public_alumni_profile(request, alumni_id):
    alumni = get_object_or_404(Alumni, pk=alumni_id)
    
    # Fetch memories for this alumni
    memories = alumni.memories.all()
    
    # Create notification only if viewer is not the profile owner
    if request.user != alumni.user:
        create_profile_view_notification(request.user, alumni.user)
    
    return render(request, 'alumni_details/alumni-profile/public-alumni-profile.html', 
                 {'alumni': alumni, 'memories': memories})


from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Alumni

# Helper function to perform the alumni search logic
@login_required_with_message
def search_alumni_query(term):
    return Alumni.objects.filter(
        Q(first_name__icontains=term) |
        Q(last_name__icontains=term) |
        Q(current_position__icontains=term) |
        Q(company_name__icontains=term) |
        Q(job_location__icontains=term)
    ).distinct()


from django.http import JsonResponse
from django.shortcuts import render
from .models import Alumni


#This is used for suggest the keywords  || or enhances the user experience by offering suggestions.
@login_required_with_message
def autocomplete(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        
        # Split the search term into words, if any
        query_parts = term.split()
        
        # Filter based on the presence of multiple parts in the query
        qs = Alumni.objects.none()
        
        # If there are multiple query parts, perform the search based on each
        if len(query_parts) > 1:
            qs = Alumni.objects.filter(
                first_name__icontains=query_parts[0],
                last_name__icontains=query_parts[-1]
            )
        else:
            qs = Alumni.objects.filter(
                Q(first_name__icontains=term) |
                Q(last_name__icontains=term) |
                Q(current_position__icontains=term) |
                Q(company_name__icontains=term) |
                Q(job_location__icontains=term)
            )
        
        # Using sets to avoid duplicates
        names = {f"{alumni.first_name} {alumni.last_name}" for alumni in qs if alumni.first_name and alumni.last_name}
        positions = {alumni.current_position for alumni in qs if alumni.current_position}
        companies = {alumni.company_name for alumni in qs if alumni.company_name}
        job_locations = {alumni.job_location for alumni in qs if alumni.job_location}

        # Combine suggestions from multiple fields
        suggestions = list(names | positions | companies | job_locations)
        
        return JsonResponse(suggestions, safe=False)
    return render(request, 'alumni_details/search.html')



#this performs the full search and renders the results page.
'''Below code '''



@login_required_with_message
def alumni_search(request):
    query = request.GET.get('alumni')
    graduation_year = request.GET.get('graduation_year')  # Graduation year filter
    job_location = request.GET.get('job_location')  # Job location filter

    # Fetch distinct graduation years and job locations for the filters
    graduation_years = Alumni.objects.values_list('graduation_year', flat=True).distinct()
    job_locations = Alumni.objects.values_list('job_location', flat=True).distinct()

    # Initialize the alumni list
    alumni_list = Alumni.objects.all()

    # Apply search query
    if query:
        query_parts = query.split()
        name_search = Alumni.objects.none()
        position_search = Alumni.objects.none()
        company_search = Alumni.objects.none()

        if len(query_parts) > 1:
            name_search = Alumni.objects.filter(
                first_name__icontains=query_parts[0],
                last_name__icontains=query_parts[-1]
            )
        else:
            name_search = Alumni.objects.filter(
                first_name__icontains=query
            ) | Alumni.objects.filter(
                last_name__icontains=query
            ) | Alumni.objects.filter(
                job_location__icontains=query
            )

        position_search = Alumni.objects.filter(current_position__icontains=query)
        company_search = Alumni.objects.filter(company_name__icontains=query)

        alumni_list = name_search | position_search | company_search

    # Apply graduation year filter
    if graduation_year:
        alumni_list = alumni_list.filter(graduation_year=graduation_year)

    # Apply job location filter
    if job_location:
        alumni_list = alumni_list.filter(job_location__icontains=job_location)

    # Paginate the results
    paginator = Paginator(alumni_list.distinct(), 5)  # 5 results per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'graduation_years': graduation_years,
        'job_locations': job_locations,
        'graduation_year': graduation_year,  # To highlight the selected graduation year
        'job_location': job_location,  # To highlight the selected job location
        'query': query,  # To preserve the search query
    }
    return render(request, 'alumni_details/alumni_search_results.html', context)



'''above code'''
# @login_required_with_message
# def alumni_search(request):
#     query = request.GET.get('alumni')
#     alumni_list = None
#     if query:
#         query_parts = query.split()
#         name_search = Alumni.objects.none()
#         position_search = Alumni.objects.none()
#         company_search = Alumni.objects.none()

#         if len(query_parts) > 1:
#             name_search = Alumni.objects.filter(
#                 first_name__icontains=query_parts[0], 
#                 last_name__icontains=query_parts[-1]
#             )
#         else:
#             name_search = Alumni.objects.filter(
#                 first_name__icontains=query
#             ) | Alumni.objects.filter(
#                 last_name__icontains=query
#             )

#         position_search = Alumni.objects.filter(
#             current_position__icontains=query
#         )

#         company_search = Alumni.objects.filter(
#             company_name__icontains=query  # Added company_name in full search
#         )

#         alumni_list = name_search | position_search | company_search
    
#     return render(request, 'alumni_details/alumni_search_results.html', {'alumni_list': alumni_list})



# '''



'''
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from .models import Alumni

# Helper function to perform the alumni search logic
def search_alumni_query(term):
    # Use a single query with Q objects for combined filtering
    return Alumni.objects.filter(
        Q(first_name__icontains=term) |
        Q(last_name__icontains=term) |
        Q(current_position__icontains=term) |
        Q(company_name__icontains=term)
    ).distinct()

# Autocomplete function with optimizations
def autocomplete(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        # Use a single query with Q objects
        qs = Alumni.objects.filter(
            Q(first_name__icontains=term) |
            Q(last_name__icontains=term) |
            Q(current_position__icontains=term) |
            Q(company_name__icontains=term)
        ).values_list('first_name', 'last_name', 'current_position', 'company_name')  # Fetch only necessary fields

        # Collecting suggestions using set comprehension
        suggestions = set()
        for first_name, last_name, current_position, company_name in qs:
            suggestions.add(f"{first_name} {last_name}")
            suggestions.add(current_position)
            suggestions.add(company_name)

        return JsonResponse(list(suggestions), safe=False)
    
    return render(request, 'alumni_details/search.html')


# Full search function with combined query for optimization
def alumni_search(request):
    query = request.GET.get('alumni')
    alumni_list = None
    if query:
        query_parts = query.split()
        # Use Q objects for combined name, position, and company search
        search_filter = Q(current_position__icontains=query) | Q(company_name__icontains=query)

        if len(query_parts) > 1:
            search_filter |= Q(first_name__icontains=query_parts[0], last_name__icontains=query_parts[-1])
        else:
            search_filter |= Q(first_name__icontains=query) | Q(last_name__icontains=query)

        alumni_list = Alumni.objects.filter(search_filter).distinct()
    
    return render(request, 'alumni_details/alumni_search_results.html', {'alumni_list': alumni_list})


'''


#  Council Members
'''  '''

from django.shortcuts import render
from .models import CouncilMember
@login_required_with_message
def council_members_view(request):
    # Fetch all council members and order by year (most recent first)
    council_members = CouncilMember.objects.select_related('alumni').order_by('-year')
    
    # Group council members by year
    grouped_council_members = {}
    for member in council_members:
        year = member.year
        if year not in grouped_council_members:
            grouped_council_members[year] = []
        grouped_council_members[year].append(member)
    
    # Defined the desired role order
    role_order = {
        'President': 1,
        'Vice President': 2,
        'Secretary': 3,
        'Joint Secretary': 4
    }

    # Sort members within each year based on the defined role order
    for year, members in grouped_council_members.items():
        members.sort(key=lambda x: role_order.get(x.role, 5))  # Use 5 as default for any undefined roles
    
    return render(request, 'alumni_details/council_member_list.html', {'grouped_council_members': grouped_council_members})




