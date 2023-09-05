from django.urls import path

from apps.team.views import EditTeamView

urlpatterns = [
    path('<int:pk>/edit/', EditTeamView.as_view(), name='edit_team'),
]
