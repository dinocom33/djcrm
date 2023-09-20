import random

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.account.decorators import superuser_access, org_owner_access
from apps.account.forms import UserLoginForm, RegisterForm, AddAgentForm, UserAccountForm, AddOrgOwnerForm, \
    ResetPasswordForm
from apps.organization.forms import AddOrganizationForm
from apps.organization.models import Organization
from apps.team.forms import AddTeamForm
from apps.team.models import Team
from apps.userprofile.forms import UserProfileForm

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
        # form.instance.organization = self.request.user.organization
        # form.team = self.request.user.team
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
        return self.request.user.is_staff or self.request.user.is_superuser or self.request.user.is_org_owner

    def get_queryset(self):
        if self.request.user.is_org_owner and not self.request.user.is_superuser:
            return Organization.objects.filter(members=self.request.user).first().members.all(

            )

        return User.objects.all().order_by('email')

    def handle_no_permission(self):
        raise Http404()


@login_required
@org_owner_access
def create_agent(request):
    teams = Team.objects.filter(organization=request.user.organization)
    if request.method == 'POST':
        form = AddAgentForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            organization = Organization.objects.filter(members=request.user).first()
            members = list(organization.members.all())
            members.append(form.instance)
            organization.members.set(members)

            messages.success(request, f'Agent {form.cleaned_data["email"]} created successfully')

            return redirect('agents')
    else:
        form = AddAgentForm(user=request.user)

    context = {
        'form': form,
        'teams': teams
    }

    return render(request, 'account/add_agent.html', context)


@login_required
@superuser_access
def add_org_owner(request):
    if request.method == 'POST':
        user_form = AddOrgOwnerForm(request.POST)
        organization_form = AddOrganizationForm(request.POST)
        team_form = AddTeamForm(request.POST)

        if user_form.is_valid() and organization_form.is_valid() and team_form.is_valid():
            user = user_form.save()
            organization = organization_form.save(commit=False)
            team = team_form.save(commit=False)
            team.name = team_form.cleaned_data['name']
            user.is_staff = True
            user.is_org_owner = True
            user.is_agent = False
            user.groups.add(1)
            organization.owner = user
            organization.save()
            team.created_by = user
            team.organization = organization
            team.save()
            organization.members.set([user])
            user.team = team
            user.password = make_password(f"{random.randint(0, 1000)}")
            user.save()

            reset_password_form = PasswordResetForm(data={'email': user.email})

            if reset_password_form.is_valid():
                reset_password_form.save(request=request)

            messages.success(request, f'Organization owner {user_form.cleaned_data["email"]} created successfully')

            return redirect('dashboard')
    else:
        user_form = AddOrgOwnerForm()
        organization_form = AddOrganizationForm()
        team_form = AddTeamForm()

    context = {
        'user_form': user_form,
        'organization_form': organization_form,
        'team_form': team_form,
    }

    return render(request, 'account/add_org_owner.html', context)


class ResetPasswordView(PasswordResetView):
    form_class = ResetPasswordForm
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
