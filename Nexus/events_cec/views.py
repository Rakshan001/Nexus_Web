from django.shortcuts import render, get_object_or_404
from .models import Event, EventImage

# View for displaying a list of all events
def event_list(request):
    events = Event.objects.all().order_by('-date')  # Ordering events by date (most recent first)
    return render(request, 'events_cec/event_list.html', {'events': events})

# View for displaying an event and its images
def event_detail(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    images = EventImage.objects.filter(event=event)  # Fetch associated images
    return render(request, 'events_cec/event_details.html', {'event': event, 'images': images})
