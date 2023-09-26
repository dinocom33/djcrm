import random

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView

from apps.account.decorators import superuser_access
from apps.account.forms import AddOrgOwnerForm
from apps.lead.models import Lead
from apps.organization.forms import AddOrganizationForm
from apps.organization.models import Organization
from apps.team.forms import AddTeamForm
from apps.team.models import Team

User = get_user_model()


class OrganizationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Organization
    template_name = 'organizations/organization_list.html'
    context_object_name = 'organizations'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams_count'] = Team.objects.filter(organization=self.request.user.organizations.first()).count()
        context['agents_count'] = Organization.objects.filter(members=self.request.user).first().members.all().count()
        context['leads_count'] = Lead.objects.filter(organization=self.request.user.organizations.first()).count()
        return context

    def get_queryset(self):
        return Organization.objects.all().order_by('name')


@login_required
@superuser_access
def add_organization(request):
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

    return render(request, 'account/../../templates/organizations/add_organization.html', context)
