from django.urls import path
from app_auth.api.views.reset_password_view import ResetPasswordView
from app_auth.api.views.user_retrieve_update_destroy_view import UserRetrieveUpdateDestroyView
from app_auth.api.views.user_creation_view import UserCreationView
from app_auth.api.views.send_verify_email_view import SendVerifyEmailView

urlpatterns = [
    path("account", UserCreationView.as_view(), name="user-post"),
    path("account/profile", UserRetrieveUpdateDestroyView.as_view(),
         name="user-put-get-del"),
    path("user/send-verify-email", SendVerifyEmailView.as_view(),
         name="send-verify-email"),
    path("user/password-reset", ResetPasswordView.as_view(),
         name="reset-password"),
]
