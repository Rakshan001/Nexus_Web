# views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Event, EventImage
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string

def event_list(request):
    all_events = Event.objects.all()  # Fetch all events
    event_type = request.GET.get('event_type')  # Get the selected event type
    category = request.GET.get('category')  # Get the selected category
    search_query = request.GET.get('search')  # Get the search query
    page = request.GET.get('page', 1)  # Get the page number

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

    # Filter by category if selected
    if category:
        all_events = all_events.filter(category=category)

    # Filter based on search query if provided
    if search_query:
        all_events = all_events.filter(event_title__icontains=search_query)

    # Paginate the events
    paginator = Paginator(all_events, 3)  # Show 5 events per page
    events = paginator.get_page(page)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        event_data = []
        for event in events:
            event_data.append({
                'title': event.event_title,
                'date': event.date.strftime('%Y-%m-%d'),
                'time': event.time.strftime('%H:%M') if event.time else '',
                'location': event.location,
                'category': event.get_category_display(),
                'poster_url': event.poster.url if event.poster else '',
                'detail_url': reverse('event_detail', args=[event.event_id])
            })
        return JsonResponse({
            'events': event_data,
            'has_next': events.has_next(),
            'next_page': events.next_page_number() if events.has_next() else None
        })

    # Get all available categories
    categories = Event.CATEGORY_CHOICES

    context = {
        'all_events': events,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category,
        'selected_event_type': event_type,
    }

    return render(request, 'events_cec/announcement.html', context)

# ... rest of your views remain the same ...

def event_detail(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    images = EventImage.objects.filter(event=event)
    return render(request, 'events_cec/event-details.html', {'event': event, 'images': images})

def gallery_view(request):
    initial_count = 2
    gallery_images = Gallery.objects.all()
    limit = request.GET.get('limit', initial_count)
    limit = int(limit)
    images_to_display = gallery_images[:limit]

    context = {
        'images': images_to_display,
        'total_count': gallery_images.count(),
        'loaded_count': len(images_to_display),
    }
    return render(request, 'events_cec/gallery.html', context)