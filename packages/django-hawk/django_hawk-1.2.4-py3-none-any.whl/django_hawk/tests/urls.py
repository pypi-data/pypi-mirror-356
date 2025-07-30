from django.urls import path

from django_hawk.tests.views import custom_header_view, simple_view

urlpatterns = [
    path(
        "test-simple-view/",
        simple_view,
        name="test_simple_view",
    ),
    path(
        "test-custom-header-view/",
        custom_header_view,
        name="custom_header_view",
    ),
]
