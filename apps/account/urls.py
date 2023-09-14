from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.account.views import RegisterView, UserLoginView, AllAgentsView, my_profile, create_agent, add_org_owner

urlpatterns = [
    path('sign-up/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', my_profile, name='profile'),
    path('add-agent/', create_agent, name='add_agent'),
    path('agents/', AllAgentsView.as_view(), name='agents'),
    path('add_org_owner/', add_org_owner, name='add_org_owner'),
]
