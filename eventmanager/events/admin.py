from django.contrib import admin
from .models import Event, Invitation, EventParticipation


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "location", "is_private", "created_by")
    list_filter = ("is_private", "date", "created_by")
    search_fields = ("title", "location", "description")
    ordering = ("-date",)
    readonly_fields = ("created_by",)
    date_hierarchy = "date"


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "status", "invited_by")
    list_filter = ("status", "event", "invited_by")
    search_fields = ("event__title", "user__username", "user__email")
    ordering = ("event",)


@admin.register(EventParticipation)
class EventParticipationAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "status")
    list_filter = ("status", "event")
    search_fields = ("event__title", "user__username", "user__email")
