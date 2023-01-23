import io

import pytest
from images.tests.factories import ImageFactory


@pytest.fixture
def image_file():
    """
    Return a 1x1 PNG.
    """
    file = io.BytesIO(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00"
        b"\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00"
        b"\x00\x00IEND\xaeB`\x82"
    )
    file.name = "image.png"
    return file


@pytest.fixture
def image_factory():
    return ImageFactory


@pytest.fixture(autouse=True)
def configure_settings(settings):
    settings.REST_FRAMEWORK = {
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": 1,
    }
