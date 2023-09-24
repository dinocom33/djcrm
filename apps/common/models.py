from django.core import validators
from django.db import models


class ContactModel(models.Model):
    email = models.EmailField(
        max_length=254,
        validators=[
            validators.EmailValidator(message="Please enter a valid email address.!@#")
        ]
    )
    subject = models.CharField(
        max_length=255
    )
    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Contact Form"
        verbose_name_plural = "Contact Forms"

    def __str__(self):
        return self.email
