from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from apps.client.models import Client
from apps.lead.forms import AddLeadForm, EditLeadForm
from apps.lead.models import Lead


@login_required
def add_lead(request):

    if request.method == 'POST':
        form = AddLeadForm(user=request.user, data=request.POST)

        if form.is_valid():
            print(request.user.organizations.first())
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.save()
            messages.success(request, f'Lead {lead.name} added successfully')
            return redirect('all_leads')
    else:
        form = AddLeadForm(user=request.user)

    context = {
        'form': form,
    }

    return render(request, 'lead/add_lead.html', context)


class AllLeadsView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'lead/all_leads.html'
    context_object_name = 'all_leads'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_agent:
            queryset = Lead.objects.filter(
                                            created_by=self.request.user,
                                            converted=False,
                                            organization=self.request.user.organizations.first(),
                                            team=self.request.user.teams.first(),
                                        ).order_by('-created_at', 'priority')
        else:
            queryset = Lead.objects.filter(converted=False,
                                           organization=self.request.user.organizations.first()
                                           ).order_by('-created_at', 'priority')
        return queryset


@login_required
def lead_details(request, pk):
    if request.user.is_agent:
        lead = get_object_or_404(Lead,
                                 created_by=request.user,
                                 organization=request.user.organizations.first(),
                                 team=request.user.teams.first(),
                                 pk=pk,
                                 )
    else:
        lead = get_object_or_404(Lead,
                                 organization=request.user.organizations.first(),
                                 pk=pk,
                                 )

    context = {
        'lead': lead
    }

    return render(request, 'lead/lead_details.html', context)


class DeleteLeadView(LoginRequiredMixin, DeleteView):
    model = Lead
    template_name = 'lead/delete_lead.html'

    def get_success_url(self):
        return reverse_lazy('all_leads')


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
        lead = get_object_or_404(Lead,
                                 created_by=request.user,
                                 pk=pk,
                                 organization=request.user.organizations.first(),
                                 team=request.user.teams.first(),
                                 )
    else:
        lead = get_object_or_404(Lead,
                                 pk=pk,
                                 organization=request.user.organizations.first(),
                                 )

    if request.method == 'POST':
        form = EditLeadForm(user=request.user, data=request.POST, instance=lead)

        if form.is_valid():
            form.save()
            messages.success(request, f'Lead {lead.name} updated successfully')
            return redirect('lead_details', pk=lead.pk)
    else:
        form = EditLeadForm(user=request.user, instance=lead)

    context = {
        'form': form,
    }

    return render(request, 'lead/edit_lead.html', context)


@login_required
def convert_to_client(request, pk):
    if request.user.is_agent:
        lead = get_object_or_404(Lead,
                                 created_by=request.user,
                                 pk=pk,
                                 organization=request.user.organizations.first(),
                                 team=request.user.teams.first(),
                                 )
    else:
        lead = get_object_or_404(Lead,
                                 pk=pk,
                                 organization=request.user.organizations.first(),
                                 )

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
