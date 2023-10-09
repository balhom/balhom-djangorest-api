from django.urls import path
from app_auth.api.views.reset_password_view import ResetPasswordView
from app_auth.api.views.user_retrieve_update_destroy_view import UserRetrieveUpdateDestroyView
from app_auth.api.views.user_creation_view import UserCreationView
from app_auth.api.views.send_verify_email_view import SendVerifyEmailView
from app_auth.api.views.auth_views import (
    AccessView,
    RefreshView,
    LogoutView
)

urlpatterns = [
    path("auth/access", AccessView.as_view(), name="access"),
    path("auth/refresh", RefreshView.as_view(), name="refresh"),
    path("auth/logout", LogoutView.as_view(), name="logout"),
    path("account", UserCreationView.as_view(), name="user-post"),
    path("account/profile", UserRetrieveUpdateDestroyView.as_view(),
         name="user-put-get-del"),
    path("user/send-verify-email", SendVerifyEmailView.as_view(),
         name="send-verify-email"),
    path("user/password-reset", ResetPasswordView.as_view(),
         name="reset-password"),
]
