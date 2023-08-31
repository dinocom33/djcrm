from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView

from apps.lead.forms import AddLeadForm
from apps.lead.models import Lead


@login_required
def add_lead(request):
    if request.method == 'POST':
        form = AddLeadForm(request.POST)

        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.save()
            return redirect('all_leads')
    else:
        form = AddLeadForm()

    context = {
        'form': form
    }

    return render(request, 'lead/add_lead.html', context)


class AllLeadsView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'lead/all_leads.html'
    context_object_name = 'all_leads'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_agent:
            queryset = Lead.objects.filter(created_by=self.request.user).order_by('-created_at', 'priority')
        else:
            queryset = Lead.objects.all().order_by('-created_at', 'priority')
        return queryset
