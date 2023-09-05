from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from apps.client.models import Client
from apps.lead.models import Lead

User = get_user_model()


@login_required
def dashboard(request):
    if request.user.is_agent:
        leads = Lead.objects.filter(created_by=request.user).order_by('-created_at')
        clients = Client.objects.filter(lead_agent=request.user).order_by('-created_at')
    else:
        leads = Lead.objects.all().order_by('-created_at')
        clients = Client.objects.all().order_by('-created_at')

    context = {
        'leads': leads,
        'clients': clients
    }

    return render(request, 'dashboard/dashboard.html', context)


class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_agent:
            context['leads'] = Lead.objects.filter(created_by=self.request.user, converted=False).order_by(
                '-created_at')[0:5]
            context['clients'] = Client.objects.filter(lead_agent=self.request.user).order_by('-created_at')[0:5]
            context['organization'] = self.request.user.organizations.filter(members=self.request.user).get()
        else:
            context['leads'] = Lead.objects.filter(converted=False).order_by('-created_at')[0:5]
            context['clients'] = Client.objects.all().order_by('-created_at')[0:5]
            context['agents'] = User.objects.filter(is_agent=True)
            context['organization'] = self.request.user.organizations.filter(members=self.request.user).get()
        return context

    def get_queryset(self):
        if self.request.user.is_agent:
            queryset = Lead.objects.filter(created_by=self.request.user, converted=False).order_by('-created_at',
                                                                                                   'priority')
        else:
            queryset = Lead.objects.filter(converted=False).order_by('-created_at', 'priority')

        return queryset
