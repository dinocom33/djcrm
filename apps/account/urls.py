from django.contrib.auth.views import LogoutView, PasswordResetConfirmView, PasswordResetCompleteView, \
    PasswordResetView, PasswordResetDoneView
from django.urls import path

from apps.account.views import UserLoginView, AllAgentsView, my_profile, create_agent, ResetPasswordView, SearchAgentView
from apps.common.views import AboutUsView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', my_profile, name='profile'),
    path('add-agent/', create_agent, name='add_agent'),
    path('agents/', AllAgentsView.as_view(), name='agents'),
    path('password-reset/', ResetPasswordView.as_view(template_name='registration/password_reset.html'),
         name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('about/', AboutUsView.as_view(), name='about'),
    path('search/', SearchAgentView.as_view(), name='agent_search'),
]
