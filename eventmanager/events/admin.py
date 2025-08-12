from django.contrib import admin
from .models import Event, Invitation


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_private', 'created_by')
    list_filter = ('is_private', 'date')
    search_fields = ('title', 'description', 'location')
    ordering = ('-date',)


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'status', 'invited_by')
    list_filter = ('status',)
    search_fields = ('event__title', 'user__username')
    ordering = ('event',)

