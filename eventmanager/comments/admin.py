from django.contrib import admin
from eventmanager.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("event", "author", "approved", "created_at")
    list_filter = ("approved", "created_at", "event")
    search_fields = ("event__title", "author__username", "text")
    ordering = ("-created_at",)
    readonly_fields = ("event", "author")
    actions = ["approve_comments", "reject_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = "Approve selected comments"

    def reject_comments(self, request, queryset):
        queryset.update(approved=False)

    reject_comments.short_description = "Reject selected comments"
