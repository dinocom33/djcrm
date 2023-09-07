from django import forms

from apps.client.models import Client


class AddClientForm(forms.ModelForm):
    # def __init__(self, user, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['team'].queryset = user.organizations.first().team_set.all()

    class Meta:
        model = Client
        fields = ['name', 'email', 'notes']


class EditClientForm(forms.ModelForm):
    # def __init__(self, user, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['team'].queryset = user.organizations.first().team_set.all()
    class Meta:
        model = Client
        fields = ['name', 'email', 'notes']