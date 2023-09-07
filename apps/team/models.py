from django.contrib.auth import get_user_model
from django.db import models

from apps.organization.models import Organization

User = get_user_model()


class Team(models.Model):
    name = models.CharField(
        max_length=255
    )

    # members = models.ForeignKey(
    #     User,
    #     related_name='teams',
    #     on_delete=models.CASCADE,
    # )

    created_by = models.ForeignKey(
        User,
        related_name='created_by',
        on_delete=models.CASCADE,
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

    def __str__(self):
        return self.name
