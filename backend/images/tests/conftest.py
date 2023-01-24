import io

import boto3
import pytest
from images.tests.factories import ImageFactory
from moto import mock_s3


@pytest.fixture(autouse=True)
def configure_settings(settings):
    settings.REST_FRAMEWORK = {
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": 1,
    }
    settings.AWS_ACCESS_KEY_ID = "testaccesskey"
    settings.AWS_SECRET_ACCESS_KEY = "testsecretaccesskey"
    settings.AWS_STORAGE_BUCKET_NAME = "testbucketname"


@pytest.fixture
def image_file():
    file = io.BytesIO(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00"
        b"\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00"
        b"\x00\x00IEND\xaeB`\x82"
    )
    file.name = "image.png"
    return file


@pytest.fixture
def text_file():
    file = io.StringIO("test\n" "file")
    file.name = "image.txt"
    return file


@pytest.fixture
def text_file_image_extension():
    file = io.StringIO("test\n" "file")
    file.name = "image.jpg"
    return file


@pytest.fixture
def image_factory():
    return ImageFactory


@pytest.fixture(scope="function")
def s3():
    with mock_s3():
        yield boto3.client("s3")
