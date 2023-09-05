from django import forms

from apps.client.models import Client


class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'notes']


class EditClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'team', 'notes']