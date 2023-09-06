from django.urls import path

from apps.team.views import EditTeamView, TeamListView

urlpatterns = [
    path('', TeamListView.as_view(), name='all_teams'),
    path('<int:pk>/edit/', EditTeamView.as_view(), name='edit_team'),
]
