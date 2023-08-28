from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

User = get_user_model()


class Lead(models.Model):

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'

    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
        (CRITICAL, 'Critical'),
    ]

    NAME_LENGTH = 255
    PRIORITY_LENGTH = max(len(p[0]) for p in PRIORITY_CHOICES)

    NEW = 'new'
    CONTACTED = 'contacted'
    WON = 'won'
    LOST = 'lost'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (WON, 'Won'),
        (LOST, 'Lost'),
        (CANCELLED, 'Cancelled'),
    ]

    STATUS_LENGTH = max(len(s[0]) for s in STATUS_CHOICES)

    name = models.CharField(
        max_length=NAME_LENGTH,
    )

    email = models.EmailField(
        validators=[
            validators.EmailValidator(),
        ],
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_by = models.ForeignKey(
        User,
        related_name='leads',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    priority = models.CharField(
        max_length=PRIORITY_LENGTH,
        choices=PRIORITY_CHOICES,
        default=LOW,
    )

    status = models.CharField(
        max_length=STATUS_LENGTH,
        choices=STATUS_CHOICES,
        default=NEW,
    )

    def __str__(self):
        return self.name
