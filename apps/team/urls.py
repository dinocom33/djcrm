from django.urls import path

from apps.team.views import EditTeamView, TeamListView, AddTeamView

urlpatterns = [
    path('', TeamListView.as_view(), name='all_teams'),
    path('add/', AddTeamView.as_view(), name='add_team'),
    path('<int:pk>/edit/', EditTeamView.as_view(), name='edit_team'),
]
