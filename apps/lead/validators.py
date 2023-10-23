from django.core.exceptions import ValidationError


def name_validator(value):
    if len(value) < 2 or len(value) > 255:
        raise ValidationError("Name must be between 2 and 50 characters")
