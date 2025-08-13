from django import forms
from django.contrib.auth import get_user_model
from django.forms import DateTimeField

from eventmanager.events.models import Event, EventParticipation


User = get_user_model()


class EventForm(forms.ModelForm):
    invited_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'is_private', 'invited_users']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your event...'
            }),
            'date': forms.DateInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event location'
            }),
            'is_private': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.date:
            self.initial['date'] = self.instance.date.strftime('%Y-%m-%dT%H:%M')


class RSVPForm(forms.ModelForm):
    class Meta:
        model = EventParticipation
        fields = ['status']
        widgets = {
            'status': forms.RadioSelect
        }
