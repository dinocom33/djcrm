from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


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
        fields = ['username', 'password', 'remember_me', 'first_name', 'last_name']


class AddAgentForm(UserCreationForm):

    def __init__(self, user, *args, **kwargs):
        super(AddAgentForm, self).__init__(*args, **kwargs)

        self.fields['team'].queryset = user.organizations.first().team_set.all()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'team']


class UserAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']