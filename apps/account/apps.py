from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.account'
    verbose_name = 'CRM Account'

    def ready(self):
        import apps.account.signals  # noqa
