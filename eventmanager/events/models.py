from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Event(models.Model):
    title = models.CharField(
        max_length=200,
    )
    description = models.TextField(
        blank=True,
    )
    date = models.DateTimeField()
    location = models.CharField(
        max_length=255,
        blank=True,
    )
    is_private = models.BooleanField(
        default=False
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_events'
    )

    participants = models.ManyToManyField(
        User,
        through='EventParticipation',
        related_name='attending_events',
        blank=True)

    def __str__(self):
        return self.title


class Invitation(models.Model):
    ATTENDANCE_STATUS = [
        ('A', 'Attending'),
        ('N', 'Not Attending'),
        ('M', 'Maybe'),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_invitations'
    )
    status = models.CharField(
        max_length=1,
        choices=ATTENDANCE_STATUS,
        default='M'
    )
    invited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_invitations'
    )

    class Meta:
        unique_together = ('event', 'user')  # Each user invited once per event

    def __str__(self):
        # username = self.user.get_username()
        return f"{self.user.username} - {self.get_status_display()} - {self.event.title}"


class EventParticipation(models.Model):
    ATTENDANCE_CHOICES = [
        ('yes', 'Going'),
        ('no', 'Not Going'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participations')
    status = models.CharField(max_length=3, choices=ATTENDANCE_CHOICES)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.get_status_display()}"
