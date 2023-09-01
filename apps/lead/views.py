from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView

from apps.lead.forms import AddLeadForm, DeleteLeadForm
from apps.lead.models import Lead

User = get_user_model()


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


@login_required()
def lead_details(request, pk):
    if request.user.is_agent:
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    else:
        lead = get_object_or_404(Lead, pk=pk)

    context = {
        'lead': lead
    }

    return render(request, 'lead/lead_details.html', context)


@login_required()
def delete_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = DeleteLeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('all_leads')
    else:
        form = DeleteLeadForm(instance=lead)

    context = {
        'form': form,
        'lead': lead,
    }

    return render(request, 'lead/delete_lead.html', context)


class DeleteLeadView(LoginRequiredMixin, DeleteView):
    model = Lead
    form_class = DeleteLeadForm
    template_name = 'lead/delete_lead.html'
    success_url = 'all_leads'


class LeadsFilterView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'lead/all_leads.html'
    context_object_name = 'all_leads'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeadsFilterView, self).get_context_data(**kwargs)
        context['status'] = self.kwargs['status']

        return context

    def get_queryset(self):
        lead_status = self.kwargs['status']
        return Lead.objects.filter(status=lead_status).order_by('-created_at')
