from django import forms
from django.http import request

from apps.lead.models import Lead
from apps.team.models import Team


class AddLeadForm(forms.ModelForm):
    # def __init__(self, user, *args, **kwargs):
    #     super(AddLeadForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['team'].queryset = user.organizations.first().team_set.all()

    class Meta:
        model = Lead
        fields = ('name', 'email', 'priority', 'status', 'notes')
        widgets = {
            'priority': forms.Select(
                choices=Lead.PRIORITY_CHOICES,
                attrs={
                    'class': 'selectpicker form-control rounded-mb-0'
                }
            ),
            'status': forms.Select(
                choices=Lead.STATUS_CHOICES,
                attrs={
                    'class': 'selectpicker form-control rounded-mb-0'
                }
            )
        }


class EditLeadForm(forms.ModelForm):
    # def __init__(self, user, *args, **kwargs):
    #     super(EditLeadForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['team'].queryset = user.organizations.first().team_set.all()

    class Meta:
        model = Lead
        fields = ('name', 'email', 'priority', 'status', 'notes')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-mb-0'}),
        }
