from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from apps.team.models import Team
from apps.userprofile.models import Userprofile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Userprofile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


@receiver(post_save, sender=User)
def add_team_to_superuser(sender, instance, created, **kwargs):
    if created:
        team, create = Team.objects.get_or_create(
            name='Admins',
        )
        instance.team = team
        instance.save()
