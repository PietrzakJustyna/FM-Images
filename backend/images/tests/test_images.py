import io

import pytest


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


@pytest.mark.django_db
def test_images__get_method_is_available__should_return_200(client):
    response = client.get("/api/images/")
    assert response.status_code == 200
