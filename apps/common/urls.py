from django.urls import path

from apps.common.views import index, contact_view

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact_view, name='contact'),
]
