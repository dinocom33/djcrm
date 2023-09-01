from django import forms

from apps.lead.models import Lead


class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('name', 'email', 'priority', 'status', 'notes')


class DeleteLeadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['hidden'] = 'hidden'
            field.required = False

    def save(self, commit=True):
        if commit:
            self.instance.delete()

        return self.instance

    class Meta:
        model = Lead
        fields = '__all__'
