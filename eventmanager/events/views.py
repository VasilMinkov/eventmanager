from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView, FormView
from eventmanager.comments.forms import CommentForm
from eventmanager.events.forms import EventForm, RSVPForm, EventSearchForm
from eventmanager.events.models import Event, EventParticipation, Invitation
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Event
from .forms import EventForm


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event-create.html'

    def get_success_url(self):
        return reverse('event-details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)

        EventParticipation.objects.create(
            event=self.object,
            user=self.request.user,
            status='yes'
        )

        if form.instance.is_private:
            invited_users = form.cleaned_data.get('invited_users')
            for user in invited_users:
                Invitation.objects.create(event=self.object, user=user)

        return response


class EventListView(ListView):
    model = Event
    template_name = 'common/homepage.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            queryset = Event.objects.filter(
                Q(created_by=user) | Q(invitations__user=user) | Q(participations__user=user)
            ).distinct()
        else:
            queryset = Event.objects.filter(is_private=False)

        queryset = queryset.filter(date__gte=timezone.now()).order_by('date')

        search_query = self.request.GET.get('search')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if date_from:
            queryset = queryset.filter(date__date__gte=date_from)

        if date_to:
            queryset = queryset.filter(date__date__lte=date_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = EventSearchForm(self.request.GET or None)
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event-details.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            participants = EventParticipation.objects.filter(event=event).select_related('user')
            try:
                participation = EventParticipation.objects.get(event=event, user=user)
                context['user_rsvp'] = participation.status
            except EventParticipation.DoesNotExist:
                context['user_rsvp'] = None
        else:
            participants = EventParticipation.objects.filter(event=event).select_related('user')
            context['user_rsvp'] = None

        context['participants'] = participants
        context['has_many_participants'] = participants.count() > 5

        context['comments'] = event.comments.filter(approved=True).order_by('-created_at')
        context['comment_form'] = CommentForm()

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


class MyEventsView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/my-events.html'
    context_object_name = 'events'

    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(
            Q(created_by=user) | Q(invitations__user=user) | Q(participations__user=user)
        ).distinct().order_by('date')


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm  # Create this form based on your Event model
    template_name = 'events/edit-event.html'

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.created_by

    def handle_no_permission(self):
        messages.error(self.request, "You can only edit events you created.")
        return redirect('event-details', pk=self.get_object().pk)

    def get_success_url(self):
        messages.success(self.request, "Event updated successfully!")
        return reverse_lazy('event-details', kwargs={'pk': self.object.pk})


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/delete-event.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.created_by

    def handle_no_permission(self):
        messages.error(self.request, "You can only delete events you created.")
        return redirect('event-details', pk=self.get_object().pk)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Event deleted successfully!")
        return super().delete(request, *args, **kwargs)
