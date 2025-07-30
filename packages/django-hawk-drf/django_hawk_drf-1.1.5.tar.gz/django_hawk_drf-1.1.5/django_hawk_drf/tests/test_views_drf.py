from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from django_hawk_drf.authentication import HawkAuthenticatedUser
from django_hawk_drf.tests.test_views import DjangoHawkViewTests, hawk_auth_sender


class DjangoRestFrameworkTests(DjangoHawkViewTests, TestCase):
    view_name = "test_view_set"

    @override_settings(
        DJANGO_HAWK={
            "HAWK_INCOMING_ACCESS_KEY": "some-id",
            "HAWK_INCOMING_SECRET_KEY": "some-secret",
        }
    )
    def test_user(self):
        """
        Test the user is now a HawkAuthenticatedUser
        """

        url = self.get_url()
        sender = hawk_auth_sender(url=url)
        response = APIClient().get(
            url,
            content_type="",
            HTTP_AUTHORIZATION=sender.request_header,
            HTTP_X_FORWARDED_FOR="1.2.3.4, 123.123.123.123",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("Content-Type" in response)
        self.assertTrue("Server-Authorization" in response)
        self.assertIsInstance(response.wsgi_request.user, HawkAuthenticatedUser)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTrue(response.wsgi_request.user.is_anonymous)

    def test_no_hawk_auth(self):
        url = self.get_url()
        response = APIClient().get(
            url,
            content_type="",
            HTTP_X_FORWARDED_FOR="1.2.3.4, 123.123.123.123",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.content,
            b'{"detail":"Authentication credentials were not provided."}',
        )
        self.assertTrue("Content-Type" in response)
        self.assertFalse("Server-Authorization" in response)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTrue(response.wsgi_request.user.is_anonymous)
