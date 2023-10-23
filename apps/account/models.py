from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from apps.account.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(
        _("email address"),
        unique=True,
        validators=[
            validators.EmailValidator(message='Please enter a valid email address!!!!'),
        ]
    )

    team = models.ForeignKey(
        'team.Team',
        related_name='agents',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    is_agent = models.BooleanField(default=True)

    is_org_owner = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
