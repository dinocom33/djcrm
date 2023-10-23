from django.core import validators
from django.db import models


class ContactModel(models.Model):
    email = models.CharField(
        max_length=50,
        validators=[
            validators.EmailValidator(message='The email address is not valid! Please try again!')
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
