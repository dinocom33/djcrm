from django.urls import path

from apps.client.views import client_details, AllClientsView, DeleteClientView, add_client, edit_client

urlpatterns = [
    path('', AllClientsView.as_view(), name='all_clients'),
    path('add/', add_client, name='add_client'),
    path('<int:pk>/details/', client_details, name='client_details'),
    path('<int:pk>/edit/', edit_client, name='edit_client'),
    path('<int:pk>/delete/', DeleteClientView.as_view(), name='delete_client'),
]
