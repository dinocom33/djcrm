from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, ListView

from apps.team.models import Team


class EditTeamView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Team
    fields = ['name']
    template_name = 'team/edit_team.html'
    success_url = '/dashboard'

    def get_success_message(self, cleaned_data):
        return f'Team {self.object.name} was successfully updated'

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user or self.request.user.is_superuser


class TeamListView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, ListView):
    model = Team
    template_name = 'team/all_teams.html'
    context_object_name = 'teams'
    success_message = 'Team was successfully updated'

    def test_func(self):
        return self.request.user.is_org_owner or self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        return Team.objects.filter(organization=self.request.user.organizations.first()).order_by('name')
