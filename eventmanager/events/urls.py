from django.urls import path
from . import views
from .views import EventCreateView, EventDetailView, RSVPView, MyEventsView, EventUpdateView, EventDeleteView

urlpatterns = [
    path('', views.EventListView.as_view(), name='home'),
    path('event-create/', EventCreateView.as_view(), name='event-create'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-details'),
    path('event/<int:pk>/rsvp/', RSVPView.as_view(), name='event-rsvp'),
    path('my-events/', MyEventsView.as_view(), name='my-events'),
    path('event/<int:pk>/edit/', EventUpdateView.as_view(), name='event-edit'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),
]
