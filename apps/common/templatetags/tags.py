from django import template
from django.contrib.auth import get_user_model

register = template.Library()

User = get_user_model()
from apps.organization.models import Organization


@register.simple_tag
def organization_name(organization):
    return organization.name
