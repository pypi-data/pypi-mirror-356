from typing import Callable, Optional

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from mohawk import Receiver

from django_hawk.settings import django_hawk_settings


class HawkResponseMiddleware(MiddlewareMixin):
    def __init__(self, get_response: Optional[Callable] = None) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if not self.get_response:
            raise Exception("get_response is not defined")

        response = self.get_response(request)

        if self.is_hawk_request(request) and not response.has_header(
            "Server-Authorization"
        ):
            hawk_receiver = self.get_receiver(request)
            if hawk_receiver:
                response["Server-Authorization"] = hawk_receiver.respond(
                    content=response.content,
                    content_type=response["Content-Type"],
                )

        return response

    def is_hawk_request(self, request: HttpRequest) -> bool:
        if "HTTP_AUTHORIZATION" not in request.META:
            return False
        return request.META.get("HTTP_AUTHORIZATION", "").startswith("Hawk ")

    def get_receiver(self, request: HttpRequest) -> Optional[Receiver]:
        hawk_receiver = getattr(request, django_hawk_settings.REQUEST_ATTR_NAME, None)
        if isinstance(hawk_receiver, Receiver):
            return hawk_receiver
        return None
