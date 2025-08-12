from django.urls import path
from . import views
from .views import EventCreateView, EventDetailView, RSVPView

urlpatterns = [
    path('', views.EventListView.as_view(), name='home'),
    path('event-create/', EventCreateView.as_view(), name='event-create'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-details'),
    path('event/<int:pk>/rsvp/', RSVPView.as_view(), name='event-rsvp'),
]
