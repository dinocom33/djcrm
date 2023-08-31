from django.urls import path

from apps.lead.views import add_lead, AllLeadsView

urlpatterns = [
    path('', AllLeadsView.as_view(), name='all_leads'),
    path('add-lead/', add_lead, name='add_lead'),
]
