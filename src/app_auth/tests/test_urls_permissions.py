import logging
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from src.app_auth.models.user_model import User
import src.core.tests.utils as test_utils
from src.keycloak_client.django_client import get_keycloak_client


class AppAuthUrlsPermissionsTests(APITestCase):
    def setUp(self):
        settings.CELERY_TASK_ALWAYS_EAGER = True

        # Avoid WARNING logs while testing wrong requests
        logging.disable(logging.WARNING)

        self.user_post_url = reverse("user-post")
        self.user_put_get_del_url = reverse("user-put-get-del")
        self.reset_password_url = reverse("reset-password")
        self.send_verify_email_url = reverse("send-verify-email")

        self.keycloak_client_mock = get_keycloak_client()

        # Test user data
        self.user_data1 = {
            "keycloak_id": self.keycloak_client_mock.keycloak_id,
            "username": self.keycloak_client_mock.username,
            "email": self.keycloak_client_mock.email,
            "password": self.keycloak_client_mock.password,
            "locale": self.keycloak_client_mock.locale,
            "pref_currency_type": "EUR",
        }
        self.user_data2 = {
            "keycloak_id": self.keycloak_client_mock.keycloak_id + "1",
            "username": "username2",
            "email": "email2@test.com",
            "password": "password1@212",
            "locale": "en",
            "pref_currency_type": "EUR",
        }
        # User creation
        User.objects.create(
            keycloak_id=self.user_data1["keycloak_id"],
        )
        User.objects.create(
            keycloak_id=self.user_data2["keycloak_id"],
        )
        return super().setUp()

    def test_user_post_url(self):
        """
        Checks permissions with User post
        """
        user_data_aux = {
            "username": "test2",
            "email": "test2@email.com",
            "password": self.keycloak_client_mock.password,
            "locale": self.keycloak_client_mock.locale,
            "pref_currency_type": "EUR",
        }
        self.keycloak_client_mock.email = user_data_aux["email"]
        self.keycloak_client_mock.keycloak_id = self.keycloak_client_mock.keycloak_id + "2"
        response = test_utils.post(
            self.client, self.user_post_url, user_data_aux)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.keycloak_client_mock.email = self.user_data1["email"]

    def test_user_patch_url(self):
        """
        Checks permissions with User patch
        """
        # Try without authentication
        user_data_aux = {"username": "test"}
        response = test_utils.patch(
            self.client, self.user_put_get_del_url, user_data_aux)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        # Authenticate
        test_utils.authenticate_user(self.client)
        # Try with authentication
        response = test_utils.patch(
            self.client, self.user_put_get_del_url, user_data_aux)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_get_url(self):
        """
        Checks permissions with User get
        """
        # Try without authentications
        response = test_utils.get(self.client, self.user_put_get_del_url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        # Authenticate user1
        test_utils.authenticate_user(self.client)
        # Try with authentication
        response = test_utils.get(self.client, self.user_put_get_del_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_del_url(self):
        """
        Checks permissions with User del
        """
        # Try without authentications
        response = test_utils.delete(self.client, self.user_put_get_del_url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        # Authenticate user1
        test_utils.authenticate_user(self.client)
        # Try with authentication
        response = test_utils.delete(self.client, self.user_put_get_del_url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_email_code_send_url(self):
        """
        Checks permissions with email code send
        """
        self.keycloak_client_mock.email_verified = False
        response = test_utils.post(
            self.client, self.send_verify_email_url, {
                "email": self.user_data1["email"]})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.keycloak_client_mock.email_verified = True

    def test_reset_password_url(self):
        """
        Checks permissions with reset password
        """
        # Try without authentication
        response = test_utils.post(
            self.client, self.reset_password_url, {})
        self.assertNotEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        # Begin process
        response = test_utils.post(
            self.client, self.reset_password_url,
            {
                "email": self.user_data1["email"]
            }
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
