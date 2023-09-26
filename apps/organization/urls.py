from django.urls import path

from apps.organization.views import OrganizationListView, add_organization

urlpatterns = [
    path('', OrganizationListView.as_view(), name='organization_list'),
    path('add-organization/', add_organization, name='add_organization'),
]
