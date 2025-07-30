import datetime

import mohawk
from django.test import override_settings
from django.urls import reverse
from freezegun import freeze_time


def hawk_auth_sender(
    url: str,
    key_id: str = "some-id",
    secret_key: str = "some-secret",
    method: str = "GET",
    content: str = "",
    content_type: str = "",
):
    credentials = {
        "id": key_id,
        "key": secret_key,
        "algorithm": "sha256",
    }
    return mohawk.Sender(
        credentials,
        url,
        method,
        content=content,
        content_type=content_type,
    )


class DjangoHawkViewTests:
    view_name: str = ""

    def get_path(self) -> str:
        return reverse(self.view_name)

    def get_url(self) -> str:
        return "http://testserver" + self.get_path()

    @override_settings(
        DJANGO_HAWK={
            "HAWK_INCOMING_ACCESS_KEY": "some-id",
            "HAWK_INCOMING_SECRET_KEY": "some-secret",
        }
    )
    def test_empty_object_returned_with_authentication(self):
        """
        If the Authorization and X-Forwarded-For headers are correct, then
        the correct, and authentic, data is returned
        """

        url = self.get_url()
        sender = hawk_auth_sender(url=url)
        response = self.client.get(
            url,
            content_type="",
            HTTP_AUTHORIZATION=sender.request_header,
            HTTP_X_FORWARDED_FOR="1.2.3.4, 123.123.123.123",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Content-Type" in response)
        self.assertTrue("Server-Authorization" in response)

    @override_settings(
        DJANGO_HAWK={
            "HAWK_INCOMING_ACCESS_KEY": "some-id",
            "HAWK_INCOMING_SECRET_KEY": "some-secret",
        }
    )
    def test_seen_nonce(self):
        """
        Test if reusing a nonce within 60 seconds is rejected
        """

        url = self.get_url()
        sender = hawk_auth_sender(url=url)
        response = self.client.get(
            url,
            content_type="",
            HTTP_AUTHORIZATION=sender.request_header,
            HTTP_X_FORWARDED_FOR="1.2.3.4, 123.123.123.123",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Content-Type" in response)
        self.assertTrue("Server-Authorization" in response)

        repeat_response = self.client.get(
            url,
            content_type="",
            HTTP_AUTHORIZATION=sender.request_header,
            HTTP_X_FORWARDED_FOR="1.2.3.4, 123.123.123.123",
        )
        self.assertEqual(repeat_response.status_code, 401)
        self.assertTrue("Content-Type" in response)
        self.assertTrue("Server-Authorization" in response)

    @override_settings(
        DJANGO_HAWK={
            "HAWK_INCOMING_ACCESS_KEY": "wrong-id",
            "HAWK_INCOMING_SECRET_KEY": "some-secret",
        }
    )
    def test_bad_credentials_mean_401_returned(self):
        """
        If the wrong credentials are used,
        then a 401 is returned
        """

        url = self.get_url()
        sender = hawk_auth_sender(url=url)
        response = self.client.get(
            url,
            content_type="",
            HTTP_AUTHORIZATION=sender.request_header,
            HTTP_X_FORWARDED_FOR="1.2.3.4, 123.123.123.123",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                "detail": "Incorrect authentication credentials.",
            },
        )
        self.assertTrue("Content-Type" in response)
        self.assertTrue("Server-Authorization" not in response)

    @override_settings(
        DJANGO_HAWK={
            "HAWK_INCOMING_ACCESS_KEY": "some-id",
            "HAWK_INCOMING_SECRET_KEY": "some-secret",
        }
    )
    def test_if_61_seconds_in_past_401_returned(self):
        """
        If the Authorization header is generated 61 seconds in the past, then a
        401 is returned
        """

        url = self.get_url()
        past = datetime.datetime.now() - datetime.timedelta(seconds=61)
        with freeze_time(past):
            auth = hawk_auth_sender(url).request_header
        response = self.client.get(
            url,
            content_type="",
            HTTP_AUTHORIZATION=auth,
            HTTP_X_FORWARDED_FOR="1.2.3.4, 123.123.123.123",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                "detail": "Incorrect authentication credentials.",
            },
        )
        self.assertTrue("Content-Type" in response)
        self.assertTrue("Server-Authorization" not in response)
