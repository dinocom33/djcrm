from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView

from apps.client.models import Client
from apps.lead.models import Lead
from apps.organization.models import Organization
from apps.team.models import Team

User = get_user_model()


class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_agent:
            context['leads'] = Lead.objects.filter(
                organization=self.request.user.organizations.first(),
                converted=False).order_by('-created_at')[0:5]
            context['clients'] = Client.objects.filter(
                organization=self.request.user.organizations.first(),
            ).order_by('-created_at')[0:5]
            context['organization'] = self.request.user.organizations.filter(members=self.request.user).get()
        elif self.request.user.is_org_owner and not self.request.user.is_superuser:
            context['leads'] = Lead.objects.filter(converted=False,
                                                   organization=self.request.user.organizations.first(),
                                                   ).order_by('-created_at')[0:5]
            context['clients'] = Client.objects.filter(organization=self.request.user.organizations.first()
                                                       ).order_by('-created_at')[0:5]
            context['agents'] = User.objects.filter(organizations=self.request.user.organizations.first())[0:5]
            context['organization'] = self.request.user.organizations.filter(members=self.request.user).get()
            context['teams'] = self.request.user.organizations.first().team_set.all()[0:5]
        else:
            context['leads'] = Lead.objects.all()[0:5]
            context['clients'] = Client.objects.all()[0:5]
            context['agents'] = User.objects.all()[0:5]
            context['organizations'] = Organization.objects.all()[0:5]
            context['teams'] = Team.objects.all()[0:5]

        return context

    def get_queryset(self):
        if self.request.user.is_agent:
            queryset = Lead.objects.filter(organization=self.request.user.organizations.first(),
                                           team=self.request.user.team,
                                           created_by=self.request.user,
                                           converted=False
                                           ).order_by('-created_at',
                                                      'priority')
        else:
            queryset = Lead.objects.filter(organization=self.request.user.organizations.first(),
                                           converted=False,
                                           ).order_by('-created_at', 'priority')

        return queryset
