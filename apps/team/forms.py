from django import forms

from .models import Team


class AddTeamForm(forms.ModelForm):
    custom_names = {'name': 'team_name'}

    def add_prefix(self, field_name):
        field_name = self.custom_names.get(field_name, field_name)
        return super(AddTeamForm, self).add_prefix(field_name)

    class Meta:
        model = Team
        fields = ['name']
