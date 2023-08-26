from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username',
                'id': 'username',
            },

        )
    )

    password = forms.CharField(
        max_length=50,
        required=True,
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password',
                'id': 'password'
            }
        )
    )

    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']
