from django.test import TestCase, override_settings
from django.urls import reverse

from django_hawk.tests.test_views import DjangoHawkViewTests, hawk_auth_sender


class DjangoViewTests(DjangoHawkViewTests, TestCase):
    view_name = "test_simple_view"


@override_settings(
    DJANGO_HAWK={
        "HAWK_INCOMING_ACCESS_KEY": "some-id",
        "HAWK_INCOMING_SECRET_KEY": "some-secret",
    }
)
class CustomHeaderViewTests(TestCase):
    def _get(self):
        url = "http://testserver" + reverse("custom_header_view")
        sender = hawk_auth_sender(url=url)

        return self.client.get(
            url,
            content_type="",
            HTTP_AUTHORIZATION=sender.request_header,
            HTTP_X_FORWARDED_FOR="1.2.3.4, 123.123.123.123",
        )

    def test_custom_header_is_in_response(self):
        response = self._get()

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Content-Type" in response)
        self.assertTrue("Server-Authorization" in response)
        self.assertEqual(response["Server-Authorization"], "custom-header-value")
