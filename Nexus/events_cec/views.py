from django.shortcuts import render, get_object_or_404
from .models import Event, EventImage
from django.utils import timezone

def event_list(request):
    all_events = Event.objects.all()  # Fetch all events
    event_type = request.GET.get('event_type')  # Get the selected event type from the request
    search_query = request.GET.get('search')  # Get the search query

    # Get current date and time
    now = timezone.now()
    current_date = now.date()
    current_time = now.time()

    # Filter events based on the selected event type
    if event_type == 'upcoming':
        all_events = all_events.filter(date__gt=now).order_by('date')
    elif event_type == 'ongoing':
        all_events = all_events.filter(
            date=current_date,
            time__gte=current_time
        ).order_by('time')
    elif event_type == 'past':
        all_events = all_events.filter(date__lt=current_date).order_by('-date')

    # Further filter based on search query if provided
    if search_query:
        all_events = all_events.filter(event_title__icontains=search_query)

    context = {
        'all_events': all_events,  # Pass the filtered events to the template
        'search_query': search_query,  # Include search query for maintaining input value
    }

    return render(request, 'events_cec/announcement.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    images = EventImage.objects.filter(event=event)
    return render(request, 'events_cec/event-details.html', {'event': event, 'images': images})




from .models import Gallery

def gallery_view(request):
    # Number of images to display initially
    initial_count = 2
    
    # Get all images, ordered by date_uploaded (most recent first)
    gallery_images = Gallery.objects.all()

    # Get the number of images to load (from query params, if provided)
    limit = request.GET.get('limit', initial_count)
    limit = int(limit)

    # Slice the queryset for the current view
    images_to_display = gallery_images[:limit]

    context = {
        'images': images_to_display,
        'total_count': gallery_images.count(),
        'loaded_count': len(images_to_display),
    }
    return render(request, 'events_cec/gallery.html', context)
