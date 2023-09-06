from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.account.forms import UserLoginForm, RegisterForm

User = get_user_model()


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'common/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f'Registration for user with email {form.cleaned_data["email"]} is successful')
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

        messages.success(self.request, f'Welcome {form.cleaned_data["username"]}!')

        return super(UserLoginView, self).form_valid(form)


@login_required
def my_profile(request):
    user = request.user
    return render(request, 'account/profile.html')


class AllAgentsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'account/all_agents.html'
    context_object_name = 'all_agents'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_org_owner or self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = self.request.user.teams.all()
        return context

    def get_queryset(self):
        queryset = User.objects.filter(is_agent=True).order_by('email')

        return queryset

    def handle_no_permission(self):
        raise Http404()
