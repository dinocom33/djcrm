from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView

from apps.client.models import Client
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
            messages.success(request, f'Lead {lead.name} added successfully')
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
            queryset = Lead.objects.filter(created_by=self.request.user, converted=False).order_by('-created_at',
                                                                                                   'priority')
        else:
            queryset = Lead.objects.filter(converted=False).order_by('-created_at', 'priority')
        return queryset


@login_required
def lead_details(request, pk):
    if request.user.is_agent:
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    else:
        lead = get_object_or_404(Lead, pk=pk)

    context = {
        'lead': lead
    }

    return render(request, 'lead/lead_details.html', context)


@login_required
def delete_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = DeleteLeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, f'Lead {lead.name} deleted successfully')
            return redirect('all_leads')
    else:
        form = DeleteLeadForm(instance=lead)

    context = {
        'form': form,
        'lead': lead,
    }

    return render(request, 'lead/delete_lead.html', context)


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


@login_required
def edit_lead(request, pk):
    if request.user.is_agent:
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    else:
        lead = get_object_or_404(Lead, pk=pk)

    if request.method == 'POST':
        form = AddLeadForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()
            messages.success(request, f'Lead {lead.name} updated successfully')
            return redirect('lead_details', pk=lead.pk)
    else:
        form = AddLeadForm(instance=lead)

    context = {
        'form': form,
    }

    return render(request, 'lead/edit_lead.html', context)


@login_required
def convert_to_client(request, pk):
    if request.user.is_agent:
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    else:
        lead = get_object_or_404(Lead, pk=pk)

    Client.objects.create(
        name=lead.name,
        email=lead.email,
        notes=lead.notes,
        lead_agent=lead.created_by,
        converted_by=request.user,
        created_at=lead.created_at
    )

    lead.converted = True
    lead.save()

    messages.success(request, f'Lead "{lead.name}" converted to client successfully')

    return redirect('all_leads')


class AllClientsView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client/all_clients.html'
    context_object_name = 'all_clients'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_agent:
            queryset = Client.objects.filter(lead_agent=self.request.user).order_by('-created_at')
        else:
            queryset = Client.objects.all().order_by('-created_at')

        return queryset
