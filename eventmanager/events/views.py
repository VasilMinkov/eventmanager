from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, FormView

from eventmanager.events.forms import EventForm, RSVPForm
from eventmanager.events.models import Event, EventParticipation


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event-create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class EventListView(ListView):
    model = Event
    template_name = 'common/homepage.html'
    context_object_name = 'events'
    ordering = ['date']


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event-details.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        user = self.request.user

        # All participants excluding the current user
        participants = event.participants.exclude(user=user).select_related('user').all()
        context['participants'] = participants

        # Current user RSVP status
        if user.is_authenticated:
            try:
                participation = event.participants.get(user=user)
                context['user_rsvp'] = participation.status
            except EventParticipation.DoesNotExist:
                context['user_rsvp'] = None
        else:
            context['user_rsvp'] = None

        # Flag if more than 5 participants
        context['has_many_participants'] = participants.count() > 5

        return context


class RSVPView(LoginRequiredMixin, FormView):
    form_class = RSVPForm
    template_name = 'events/rsvp.html'

    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form(self):
        # Prefill form if user already RSVP'd
        try:
            participation = EventParticipation.objects.get(user=self.request.user, event=self.event)
            return self.form_class(instance=participation, **self.get_form_kwargs())
        except EventParticipation.DoesNotExist:
            return self.form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        participation = form.save(commit=False)
        participation.user = self.request.user
        participation.event = self.event
        participation.save()
        return redirect(reverse('event-details', kwargs={'pk': self.event.pk}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.event
        return context


