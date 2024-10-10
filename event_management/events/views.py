from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, RSVP, Review
from .forms import EventForm, ReviewForm


def event_list(request):
    events = Event.objects.filter(is_public=True).order_by('-start_time')
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    reviews = Review.objects.filter(event=event)
    return render(request, 'events/event_detail.html', {'event': event, 'reviews': reviews})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})


@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user != event.organizer:
        return redirect('event_detail', pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)

    return render(request, 'events/edit_event.html', {'form': form})


@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user == event.organizer:
        event.delete()
        return redirect('event_list')
    return redirect('event_detail', pk=pk)


@login_required
def add_review(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.event = event
            review.save()
            return redirect('event_detail', pk=event_id)
    else:
        form = ReviewForm()
    return render(request, 'events/add_review.html', {'form': form})
