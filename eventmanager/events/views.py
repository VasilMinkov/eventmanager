from django.shortcuts import render
from django.views.generic import TemplateView


class EventListView(TemplateView):
    template_name = 'common/homepage.html'