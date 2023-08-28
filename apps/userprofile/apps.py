from django.apps import AppConfig


class UserprofileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.userprofile'
    verbose_name = 'User Profile'

    def ready(self):
        import apps.userprofile.signals
