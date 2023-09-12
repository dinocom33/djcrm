from django.urls import path

from apps.common.views import index, ContactUsView

urlpatterns = [
    path('', index, name='index'),
    path('contact/', ContactUsView.as_view(), name='contact'),
]
