from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from apps.lead.validators import name_validator
from apps.organization.models import Organization
from apps.team.models import Team

User = get_user_model()


class Client(models.Model):
    NAME_LENGTH = 50

    name = models.CharField(
        max_length=NAME_LENGTH,
        validators=[
            name_validator,
        ]
    )

    email = models.CharField(
        max_length=50,
        validators=[
            validators.EmailValidator(message='The email address is not valid! Please try again!'),
        ],
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    converted_by = models.ForeignKey(
        User,
        related_name='clients',
        on_delete=models.CASCADE
    )

    lead_agent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    team = models.ForeignKey(
        Team,
        related_name='clients',
        on_delete=models.CASCADE
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # slug = AutoSlugField(
    #     populate_from='name',
    #     unique=True
    # )

    def save(self, *args, **kwargs):
        if not self.organization_id:
            self.organization = self.converted_by.organizations.first()

        if not self.team_id:
            self.team = self.converted_by.team

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
