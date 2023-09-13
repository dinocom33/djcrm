from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from apps.organization.models import Organization
from apps.team.models import Team

User = get_user_model()


@receiver(post_save, sender=User)
def create_super_user(sender, instance, created, **kwargs):
    if instance.is_superuser:
        organization, create = Organization.objects.get_or_create(
            name='Super Admin'
        )

        organization.members.add(instance)

        team, create = Team.objects.get_or_create(
            name='Admins',
        )

        instance.team = team

