from django import forms

from apps.organization.models import Organization


class AddOrganizationForm(forms.ModelForm):

    custom_names = {'name': 'organization_name'}

    def add_prefix(self, field_name):
        field_name = self.custom_names.get(field_name, field_name)
        return super(AddOrganizationForm, self).add_prefix(field_name)

    class Meta:
        model = Organization
        fields = ['name']
