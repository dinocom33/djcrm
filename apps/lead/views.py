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
            return redirect('dashboard')
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
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_agent:
            queryset = Lead.objects.filter(created_by=self.request.user)
        else:
            queryset = Lead.objects.all()
        return queryset
