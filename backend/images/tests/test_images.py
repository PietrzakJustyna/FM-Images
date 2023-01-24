import pytest
from images.models import Image
from moto import mock_s3
from PIL import Image as PILImage

# Test not allowed HTTP methods


@pytest.mark.django_db
def test_images__put_method_is_not_available__should_return_405(client):
    response = client.put("/api/images/")
    assert response.status_code == 405


@pytest.mark.django_db
def test_images__delete_method_is_not_available__should_return_405(client):
    response = client.delete("/api/images/")
    assert response.status_code == 405


@pytest.mark.django_db
def test_images__delete_method_is_not_available__should_return_405(client):
    response = client.patch("/api/images/")
    assert response.status_code == 405


# Test get images


@mock_s3
@pytest.mark.django_db
def test_images__get_images__should_list_images(client, image_factory, s3, settings):
    s3.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    image = image_factory()
    response = client.get("/api/images/")
    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["results"][0]["title"] == image.title


@mock_s3
@pytest.mark.django_db
def test_images__get_images_filter_by_title__should_list_images_meeting_criteria(
    client, image_factory, s3, settings
):
    s3.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    image = image_factory(title="My Beautiful Image")
    image_factory()
    response = client.get("/api/images/?title=beaut")
    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["results"][0]["title"] == image.title


@mock_s3
@pytest.mark.django_db
def test_images__get_images_pagination__should_paginate_resulting_data(
    client, image_factory, s3, settings
):
    s3.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    image_factory()
    image_factory()
    response = client.get("/api/images/")
    assert response.status_code == 200
    assert response.json()["count"] == 2
    assert response.json()["next"] is not None
    assert len(response.json()["results"]) == 1


@mock_s3
@pytest.mark.django_db
def test_images__get_images_by_existing_id__should_return_image_data(
    client, image_factory, s3, settings
):
    s3.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    image = image_factory()
    response = client.get(f"/api/images/{image.id}/")
    assert response.status_code == 200
    assert response.json()["title"] == image.title


@mock_s3
@pytest.mark.django_db
def test_images__get_images_by_non_existing_id__should_return_404(
    client, image_factory, s3, settings
):
    s3.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    image = image_factory()
    response = client.get(f"/api/images/{image.id + 1}/")
    assert response.status_code == 404


# Test adding new images


@mock_s3
@pytest.mark.django_db
def test_images__add_image__image_is_added_successfully(
    client, image_file, s3, settings
):
    s3.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    data = {"title": "test", "width": 2, "height": 2, "image_file": image_file}
    response = client.post("/api/images/", data=data)
    assert response.status_code == 201
    assert Image.objects.count() == 1
    assert Image.objects.first().title == "test"


@pytest.mark.django_db
def test_images__add_image_incorrect_height_width_data_format__image_addition_fails(
    client, image_file
):
    data = {"title": "test", "width": "a", "height": "a", "image_file": image_file}
    response = client.post("/api/images/", data=data)
    assert response.status_code == 400
    assert response.json()["height"] == ["A valid integer is required."]
    assert response.json()["width"] == ["A valid integer is required."]
    assert Image.objects.count() == 0


@pytest.mark.django_db
def test_images__add_image_no_image_file__image_addition_fails(client):
    data = {"title": "test", "width": 1, "height": 1}
    response = client.post("/api/images/", data=data)
    assert response.status_code == 400
    assert response.json()["image_file"] == ["No file was submitted."]
    assert Image.objects.count() == 0


@pytest.mark.django_db
def test_images__add_image_missing_post_data__image_addition_fails(client, image_file):
    data = {"image_file": image_file}
    response = client.post("/api/images/", data=data)
    assert response.status_code == 400
    assert response.json()["height"] == ["This field is required."]
    assert response.json()["width"] == ["This field is required."]
    assert response.json()["title"] == ["This field is required."]
    assert Image.objects.count() == 0


@pytest.mark.django_db
def test_images__add_image_negative_width_height_data__image_addition_fails(
    client, image_file
):
    data = {"title": "test", "width": -2, "height": -2, "image_file": image_file}
    response = client.post("/api/images/", data=data)
    assert response.status_code == 400
    assert response.json()["height"] == [
        "Ensure this value is greater than or equal to 0."
    ]
    assert response.json()["width"] == [
        "Ensure this value is greater than or equal to 0."
    ]
    assert Image.objects.count() == 0


@pytest.mark.django_db
def test_images__add_image_not_allowed_file_extension__image_addition_fails(
    client, text_file
):
    data = {"title": "test", "width": 2, "height": 2, "image_file": text_file}
    response = client.post("/api/images/", data=data)
    assert response.status_code == 400
    assert response.json()["image_file"] == [
        "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
    ]
    assert Image.objects.count() == 0


@pytest.mark.django_db
def test_images__add_image_not_allowed_file_format__image_addition_fails(
    client, text_file_image_extension
):
    data = {
        "title": "test",
        "width": 2,
        "height": 2,
        "image_file": text_file_image_extension,
    }
    response = client.post("/api/images/", data=data)
    assert response.status_code == 400
    assert response.json()["image_file"] == [
        "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
    ]
    assert Image.objects.count() == 0


@mock_s3
@pytest.mark.django_db
def test_images__add_image_resizes_image__image_is_resized(
    client, image_file, s3, settings
):
    s3.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    data = {"title": "test", "width": 150, "height": 150, "image_file": image_file}
    response = client.post("/api/images/", data=data)
    image = PILImage.open(image_file)
    assert image.width != 150
    assert image.height != 150
    assert response.status_code == 201
    assert Image.objects.first().image_file.width == 150
    assert Image.objects.first().image_file.height == 150
