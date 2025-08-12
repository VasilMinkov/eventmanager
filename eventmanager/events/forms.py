from django import forms
from django.forms import DateTimeField

from eventmanager.events.models import Event, EventParticipation


class EventForm(forms.ModelForm):
    date = DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']


class RSVPForm(forms.ModelForm):
    class Meta:
        model = EventParticipation
        fields = ['status']
        widgets = {
            'status': forms.RadioSelect
        }