from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView

from apps.client.forms import AddClientForm
from apps.client.models import Client


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


@login_required()
def add_client(request):
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.converted_by = request.user
            form.lead_agent = request.user
            form.save()

            messages.success(request, f'Client "{form.name}" added successfully')

            return redirect('all_clients')
    else:
        form = AddClientForm()

    context = {
        'form': form
    }

    return render(request, 'client/add_client.html', context)


@login_required
def client_details(request, pk):
    if request.user.is_agent:
        client = Client.objects.filter(lead_agent=request.user, pk=pk).get()
    else:
        client = Client.objects.get(pk=pk)

    context = {
        'client': client
    }

    return render(request, 'client/client_details.html', context)


@login_required
def edit_client(request, pk):
    if request.user.is_agent:
        client = Client.objects.filter(lead_agent=request.user, pk=pk).get()
    else:
        client = Client.objects.get(pk=pk)

    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, f'Client "{client.name}" updated successfully')
            return redirect('all_clients')
    else:
        form = AddClientForm(instance=client)

    context = {
        'form': form
    }

    return render(request, 'client/edit_client.html', context)


class DeleteClientView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'client/delete_client.html'

    def get_success_url(self):
        return reverse_lazy('all_clients')
