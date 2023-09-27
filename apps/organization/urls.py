from django.urls import path

from apps.organization.views import OrganizationListView, add_organization, edit_organization

urlpatterns = [
    path('', OrganizationListView.as_view(), name='organization_list'),
    path('add/', add_organization, name='add_organization'),
    path('edit/<int:pk>/', edit_organization, name='organization_edit'),
]
