from django import forms

from apps.team.models import Team


class AddTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']
