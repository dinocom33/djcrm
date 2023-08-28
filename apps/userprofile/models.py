from django.contrib.auth import get_user_model
from django.db import models
from django.utils.html import mark_safe

User = get_user_model()


class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
