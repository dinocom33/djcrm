from django.urls import path

from apps.lead.views import add_lead, AllLeadsView, LeadsFilterView, lead_details, delete_lead, edit_lead, \
    convert_to_client

urlpatterns = [
    path('', AllLeadsView.as_view(), name='all_leads'),
    path('<int:pk>/', lead_details, name='lead_details'),
    path('<int:pk>/edit/', edit_lead, name='edit_lead'),
    path('<int:pk>/delete/', delete_lead, name='delete_lead'),
    path('<int:pk>/convert-to-client/', convert_to_client, name='convert_to_client'),
    path('filtered/<str:status>/', LeadsFilterView.as_view(), name='leads_filter'),
    path('add-lead/', add_lead, name='add_lead'),
]
