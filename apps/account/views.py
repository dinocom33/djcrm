from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.account.forms import UserLoginForm, RegisterForm


class RegisterView(CreateView):
    template_name = 'common/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super(RegisterView, self).form_valid(form)


class UserLoginView(LoginView):
    template_name = 'common/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super(UserLoginView, self).form_valid(form)
