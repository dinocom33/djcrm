from django.urls import path

from apps.client.views import AllClientsView, DeleteClientView, add_client, edit_client, \
    ClientDetailsView, SearchClientView

urlpatterns = [
    path('', AllClientsView.as_view(), name='all_clients'),
    path('add/', add_client, name='add_client'),
    path('<int:pk>/details/', ClientDetailsView.as_view(), name='client_details'),
    path('<int:pk>/edit/', edit_client, name='edit_client'),
    path('<int:pk>/delete/', DeleteClientView.as_view(), name='delete_client'),
    path('search/', SearchClientView.as_view(), name='client_search'),
]
