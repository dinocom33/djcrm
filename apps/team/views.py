from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

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
