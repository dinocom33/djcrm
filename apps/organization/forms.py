from django import forms

from apps.organization.models import Organization


class AddOrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name']
