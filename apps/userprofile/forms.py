from django import forms
from django.contrib.auth import get_user_model

from apps.userprofile.models import Userprofile

User = get_user_model()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['avatar', 'bio']
