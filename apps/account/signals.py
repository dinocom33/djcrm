from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from apps.organization.models import Organization

User = get_user_model()


@receiver(post_save, sender=User)
def create_super_user(sender, instance, created, **kwargs):
    if instance.is_superuser:

        organization = Organization.objects.filter(name='Super Admin').first()

        if not organization:
            Organization.objects.create(
                name='Super Admin',
                owner=instance
            )
            instance.organization.members.add(instance)
        else:
            organization.members.add(instance)
