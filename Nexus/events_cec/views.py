# views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Event, EventImage, Gallery
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
# views.py
# views.py
def event_list(request):
    all_events = Event.objects.all()
    event_type = request.GET.get('event_type')
    category = request.GET.get('category')
    search_query = request.GET.get('search')
    page = request.GET.get('page', 1)

    now = timezone.now()
    current_date = now.date()
    current_time = now.time()

    # Default ordering by date
    all_events = all_events.order_by('-date', '-time')  # Notice the minus sign for descending order

    if event_type == 'upcoming':
        all_events = all_events.filter(date__gte=current_date)
    elif event_type == 'ongoing':
        all_events = all_events.filter(
            date=current_date,
            time__lte=current_time
        )
    elif event_type == 'past':
        all_events = all_events.filter(date__lt=current_date)

    if category:
        all_events = all_events.filter(category=category)

    if search_query:
        all_events = all_events.filter(event_title__icontains=search_query)

    paginator = Paginator(all_events, 3)
    events = paginator.get_page(page)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        event_data = []
        for event in events:
            # Determine event status
            if event.date > current_date:
                event_status = 'Upcoming'
            elif event.date == current_date:
                if event.time and event.time >= current_time:
                    event_status = 'Ongoing'
                else:
                    event_status = 'Past'
            else:
                event_status = 'Past'

            event_data.append({
                'title': event.event_title,
                'date': event.date.strftime('%Y-%m-%d'),
                'time': event.time.strftime('%H:%M') if event.time else '',
                'location': event.location,
                'category': event.get_category_display(),
                'poster_url': event.poster.url if event.poster else '',
                'detail_url': reverse('event_detail', args=[event.event_id]),
                'status': event_status
            })
        return JsonResponse({
            'events': event_data,
            'has_next': events.has_next(),
            'next_page': events.next_page_number() if events.has_next() else None
        })

    # Add status to initial events for template
    for event in events:
        if event.date > current_date:
            event.status = 'Upcoming'
        elif event.date == current_date:
            if event.time and event.time >= current_time:
                event.status = 'Ongoing'
            else:
                event.status = 'Past'
        else:
            event.status = 'Past'

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