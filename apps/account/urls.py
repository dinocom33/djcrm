from django.contrib.auth.views import LogoutView, PasswordResetConfirmView, PasswordResetCompleteView, \
    PasswordResetView, PasswordResetDoneView
from django.urls import path

from apps.account.views import RegisterView, UserLoginView, AllAgentsView, my_profile, create_agent, add_org_owner, \
    ResetPasswordView

urlpatterns = [
    path('sign-up/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', my_profile, name='profile'),
    path('add-agent/', create_agent, name='add_agent'),
    path('agents/', AllAgentsView.as_view(), name='agents'),
    path('add_org_owner/', add_org_owner, name='add_org_owner'),
    path('password-reset/', ResetPasswordView.as_view(template_name='registration/password_reset.html'),
         name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]
