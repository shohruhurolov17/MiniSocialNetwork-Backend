from django.urls import path
from apps.users.views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserDetailView,
    VerifyEmailView,
    SendVerificationEmailView
)


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/verify/<str:signed_data>/', VerifyEmailView.as_view(), name='verify_email'),
    path('auth/send-verification/', SendVerificationEmailView.as_view(), name='send_verification'),
    path('auth/login/', LoginView.as_view(), name='auth_login'),
    path('auth/log-out/', LogoutView.as_view(), name='auth_logout'),
    path('user/profile/', UserDetailView.as_view(), name='user_detail')
]