from django.db import models
from django.conf import settings
from eventmanager.events.models import Event


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # Moderator approval

    def __str__(self):
        return f"Comment by {self.author} on {self.event}"
