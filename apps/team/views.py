from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, ListView, CreateView

from apps.team.models import Team


class EditTeamView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Team
    fields = ['name']
    template_name = 'team/edit_team.html'
    success_url = '/teams'

    def get_success_message(self, cleaned_data):
        return f'Team {self.object.name} was successfully updated'

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user or self.request.user.is_superuser or self.request.user.is_org_owner


class TeamListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Team
    template_name = 'team/all_teams.html'
    context_object_name = 'teams'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_org_owner or self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        if self.request.user.is_org_owner and not self.request.user.is_superuser:
            return Team.objects.filter(organization=self.request.user.organizations.first()).order_by('name')

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