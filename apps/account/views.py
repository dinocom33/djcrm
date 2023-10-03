import random

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from apps.account.decorators import superuser_access, org_owner_access
from apps.account.forms import UserLoginForm, AddAgentForm, UserAccountForm, AddOrgOwnerForm, ResetPasswordForm
from apps.organization.forms import AddOrganizationForm
from apps.organization.models import Organization
from apps.team.forms import AddTeamForm
from apps.team.models import Team
from apps.userprofile.forms import UserProfileForm

User = get_user_model()


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
def my_profile(request, pk):
    user = User.objects.filter(pk=pk).get()
    teams = Team.objects.filter(organization=user.organizations.first())
    if request.method == 'POST':
        user_form = UserAccountForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Profile updated successfully')

            return redirect('profile', pk=user.pk)
    else:
        user_form = UserAccountForm(instance=user)
        profile_form = UserProfileForm(instance=user.userprofile)

    contex = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user,
        'teams': teams,
    }

    return render(request, 'account/profile.html', contex)


class AllAgentsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'account/all_agents.html'
    context_object_name = 'all_agents'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_org_owner

    def get_queryset(self):
        if self.request.user.is_org_owner and not self.request.user.is_superuser:
            return Organization.objects.filter(members=self.request.user).first().members.all()

        return User.objects.all().order_by('email')

    def handle_no_permission(self):
        raise Http404()


@login_required
@org_owner_access
def create_agent(request):
    teams = Team.objects.filter(organization=request.user.organizations.first())
    if request.method == 'POST':
        form = AddAgentForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            organization = Organization.objects.filter(members=request.user).first()
            members = list(organization.members.all())
            members.append(form.instance)
            organization.members.set(members)

            user.password = make_password(f"{random.randint(0, 1000)}")
            user.save()

            reset_password_form = PasswordResetForm(data={'email': user.email})

            if reset_password_form.is_valid():
                reset_password_form.save(request=request)

            messages.success(request, f'Agent {form.cleaned_data["email"]} created successfully')

            return redirect('agents')
    else:
        form = AddAgentForm(user=request.user)

    context = {
        'form': form,
        'teams': teams
    }

    return render(request, 'account/add_agent.html', context)


class ResetPasswordView(PasswordResetView):
    form_class = ResetPasswordForm
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class SearchAgentView(ListView):
    model = User
    template_name = 'account/agent_search_results.html'
    context_object_name = 'agent_search_results'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return User.objects.filter(Q(email__icontains=query) |
                                       Q(first_name__icontains=query) |
                                       Q(last_name__icontains=query),
                                       organizations=self.request.user.organization).order_by('-date_joined')

        return User.objects.filter(organizations=self.request.user.organization)
