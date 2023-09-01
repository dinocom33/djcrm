from django.urls import path

from apps.lead.views import add_lead, AllLeadsView, LeadsFilterView

urlpatterns = [
    path('', AllLeadsView.as_view(), name='all_leads'),
    path('filtered/<str:status>/', LeadsFilterView.as_view(), name='leads_filter'),
    path('add-lead/', add_lead, name='add_lead'),
]
