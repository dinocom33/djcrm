from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Organization(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    members = models.ManyToManyField(
        User,
        related_name='organizations',
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name
