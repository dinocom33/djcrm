from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, CreateView, DeleteView, DetailView

from apps.team.models import Team


class EditTeamView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Team
    fields = ['name']
    template_name = 'team/edit_team.html'

    def get_success_url(self):
        return reverse_lazy('all_teams')

    def get_success_message(self, cleaned_data):
        return f'Team {self.object.name} was successfully updated'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_org_owner


class TeamListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Team
    template_name = 'team/all_teams.html'
    context_object_name = 'teams'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_org_owner or self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        if self.request.user.is_org_owner and not self.request.user.is_superuser:
            return Team.objects.filter(organization=self.request.user.organizations.first()).order_by('-created_at',
                                                                                                      'name')

        return Team.objects.all().order_by('name')


class AddTeamView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Team
    fields = ['name']
    template_name = 'team/add_team.html'
    success_url = '/teams'

    def test_func(self):
        return self.request.user.is_org_owner or self.request.user.is_staff or self.request.user.is_superuser

    def get_success_message(self, cleaned_data):
        return f'Team {self.object.name} was successfully added'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.organization = self.request.user.organizations.first()

        return super().form_valid(form)


class DeleteTeamView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Team
    template_name = 'team/delete_team.html'
    success_url = '/teams'

    def test_func(self):
        return self.request.user.is_org_owner or self.request.user.is_superuser


class SearchTeamView(ListView):
    model = Team
    template_name = 'team/team_search_results.html'
    context_object_name = 'team_search_results'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Team.objects.filter(Q(name__icontains=query),
                                       organization=self.request.user.organization).order_by('-created_at')

        return Team.objects.filter(organization=self.request.user.organization).order_by('-created_at')
