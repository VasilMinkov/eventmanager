from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .forms import CommentForm
from eventmanager.events.models import Event


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        event = get_object_or_404(Event, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.author = request.user
            comment.save()
        return redirect('event_details', pk=event.pk)