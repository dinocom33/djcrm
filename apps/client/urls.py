from django.urls import path

from apps.lead.views import AllClientsView

urlpatterns = [
    path('', AllClientsView.as_view(), name='all_clients'),
]
