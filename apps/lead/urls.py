from django.urls import path

from apps.lead.views import (add_lead, AllLeadsView, LeadsFilterView, edit_lead, convert_to_client, DeleteLeadView,
                             DetailLeadView, SearchLeadView)

urlpatterns = [
    path('', AllLeadsView.as_view(), name='all_leads'),
    path('<int:pk>/', DetailLeadView.as_view(), name='lead_details'),
    path('<int:pk>/edit/', edit_lead, name='edit_lead'),
    path('<int:pk>/delete/', DeleteLeadView.as_view(), name='delete_lead'),
    path('<int:pk>/convert-to-client/', convert_to_client, name='convert_to_client'),
    path('filtered/<str:status>/', LeadsFilterView.as_view(), name='leads_filter'),
    path('add-lead/', add_lead, name='add_lead'),
    path('search/', SearchLeadView.as_view(), name='lead_search'),
]
