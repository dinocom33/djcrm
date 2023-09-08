from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from apps.client.models import Client
from apps.lead.models import Lead

User = get_user_model()


class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_agent:
            context['leads'] = Lead.objects.filter(
                organization=self.request.user.organizations.first(),
                # team=self.request.user.team,
                # created_by=self.request.user,
                converted=False).order_by('-created_at')[0:5]
            context['clients'] = Client.objects.filter(
                # lead_agent=self.request.user,
                organization=self.request.user.organizations.first(),
                # team=self.request.user.team,
            ).order_by('-created_at')[0:5]
            context['organization'] = self.request.user.organizations.filter(members=self.request.user).get()
        else:
            context['leads'] = Lead.objects.filter(converted=False,
                                                   organization=self.request.user.organizations.first(),
                                                   ).order_by('-created_at')[0:5]
            context['clients'] = Client.objects.filter(organization=self.request.user.organizations.first()
                                                       ).order_by('-created_at')[0:5]
            context['agents'] = User.objects.filter(organizations=self.request.user.organization,
                                                    )
            context['organization'] = self.request.user.organizations.filter(members=self.request.user).get()
            context['teams'] = self.request.user.organization.team_set.all()
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
