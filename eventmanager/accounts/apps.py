from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "eventmanager.accounts"

    def ready(self):
        from django.db.models.signals import post_migrate
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from django.apps import apps

        def create_groups(sender, **kwargs):
            models_to_grant = [
                ("events", "Event"),
                ("events", "Invitation"),
                ("events", "EventParticipation"),
                ("comments", "Comment"),
            ]

            perms = []
            for app_label, model_name in models_to_grant:
                Model = apps.get_model(app_label, model_name)
                ct = ContentType.objects.get_for_model(Model)
                for action in ("add", "change", "delete", "view"):
                    codename = f"{action}_{Model._meta.model_name}"
                    try:
                        perms.append(Permission.objects.get(content_type=ct, codename=codename))
                    except Permission.DoesNotExist:
                        pass

            managers, _ = Group.objects.get_or_create(name="Event Managers")
            managers.permissions.set(perms)
            managers.save()

            superadmins, _ = Group.objects.get_or_create(name="Superadmins")
            superadmins.permissions.set(perms)
            superadmins.save()

        post_migrate.connect(create_groups, sender=self)
