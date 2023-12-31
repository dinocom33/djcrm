from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView

from apps.client.forms import AddClientForm, EditClientForm
from apps.client.models import Client


class AllClientsView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client/all_clients.html'
    context_object_name = 'all_clients'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_agent:
            queryset = Client.objects.filter(
                # lead_agent=self.request.user,
                organization=self.request.user.organizations.first(),
                # team=self.request.user.team,
            ).order_by('-created_at')
        elif self.request.user.is_org_owner and not self.request.user.is_superuser:
            queryset = Client.objects.filter(
                organization=self.request.user.organization
            ).order_by('-created_at')
        else:
            queryset = Client.objects.all().order_by('-created_at')

        return queryset


@login_required()
def add_client(request):
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.converted_by = request.user
            client.lead_agent = request.user
            client.save()

            messages.success(request, f'Client "{client.name}" added successfully')

            return redirect('all_clients')
    else:
        form = AddClientForm()

    context = {
        'form': form
    }

    return render(request, 'client/add_client.html', context)


class ClientDetailsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    template_name = 'client/client_details.html'
    context_object_name = 'client'

    def test_func(self):
        return self.request.user.is_org_owner or self.request.user.is_staff or self.request.user.clients.filter(
            pk=self.kwargs['pk']).get()

    def get_context_data(self, **kwargs):
        context = super(ClientDetailsView, self).get_context_data(**kwargs)
        context['client'] = Client.objects.filter(pk=self.kwargs['pk']).get()

        return context


@login_required
def edit_client(request, pk):
    if request.user.is_agent:
        client = Client.objects.filter(
            lead_agent=request.user,
            pk=pk,
            organization=request.user.organizations.first(),
            team=request.user.team,
        ).get()
    else:
        client = Client.objects.get(
            pk=pk,
            organization=request.user.organizations.first(),
        )

    if request.method == 'POST':
        form = EditClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()

            messages.success(request, f'Client "{client.name}" updated successfully')

            return redirect('client_details', pk=client.pk)
    else:
        form = EditClientForm(instance=client)

    context = {
        'form': form
    }

    return render(request, 'client/edit_client.html', context)


class DeleteClientView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'client/delete_client.html'

    def get_success_url(self):
        return reverse_lazy('all_clients')


class SearchClientView(ListView):
    model = Client
    template_name = 'client/client_search_results.html'
    context_object_name = 'client_search_results'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Client.objects.filter(Q(name__icontains=query) |
                                         Q(email__icontains=query),
                                         organization=self.request.user.organizations.first()).order_by('-created_at')

        return Client.objects.filter(organization=self.request.user.organizations.first()).order_by('-created_at')
