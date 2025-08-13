from django.db.models.signals import post_save
from eventmanager.accounts.models import UserProfile
from eventmanager.comments.models import Comment
from eventmanager.events.models import User, Event
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == 'accounts':
        moderators, created = Group.objects.get_or_create(name='Moderators')
        event_ct = ContentType.objects.get_for_model(Event)
        comment_ct = ContentType.objects.get_for_model(Comment)

        perms = Permission.objects.filter(
            content_type__in=[event_ct, comment_ct],
            codename__in=['change_event', 'delete_event', 'change_comment', 'delete_comment']
        )
        moderators.permissions.set(perms)

        Group.objects.get_or_create(name='Users')
