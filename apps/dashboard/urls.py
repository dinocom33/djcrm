from django.urls import path

from apps.dashboard.views import dashboard, DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]
