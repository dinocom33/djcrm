from django import forms

from apps.lead.models import Lead


class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('name', 'email', 'priority', 'status', 'notes')


class EditLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('name', 'email', 'team', 'priority', 'status', 'notes')