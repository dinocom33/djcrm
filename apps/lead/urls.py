from django.urls import path

from apps.lead.views import add_lead, AllLeadsView, LeadsFilterView, lead_details, delete_lead, DeleteLeadView

urlpatterns = [
    path('', AllLeadsView.as_view(), name='all_leads'),
    path('<int:pk>/', lead_details, name='lead_details'),
    path('<int:pk>/delete/', delete_lead, name='delete_lead'),
    path('filtered/<str:status>/', LeadsFilterView.as_view(), name='leads_filter'),
    path('add-lead/', add_lead, name='add_lead'),
]
