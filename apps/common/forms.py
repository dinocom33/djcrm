from django import forms

from apps.common.models import ContactModel


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = ['email', 'subject', 'message']
