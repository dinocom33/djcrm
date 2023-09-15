from django import forms

from .models import Team


class AddTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']
