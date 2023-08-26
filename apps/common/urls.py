from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.common.views import index, RegisterView, UserLoginView

urlpatterns = [
    path('', index, name='index'),
    path('sign-up/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
