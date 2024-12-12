import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from cars.models import Car


@pytest.mark.django_db
def test_obtain_auth_token_success(api_client):
    User.objects.create_user(username="testuser", password="password")
    response = api_client.post(
        "/api/token/", {"username": "testuser", "password": "password"}
    )
    assert response.status_code == 200
    assert "token" in response.data


@pytest.mark.django_db
def test_obtain_auth_token_failure(user, api_client):
    response = api_client.post(
        "/api/token/", {"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "error" in response.data


@pytest.mark.django_db
def test_car_list(api_client, user, car, car2):
    response = api_client.get("/api/cars/")
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_car_create(api_client, user):
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = api_client.post(
        "/api/cars/create/",
        {"make": "test", "model": "test", "year": 4321, "description": "test"},
    )
    assert response.status_code == 201
    assert response.data["make"] == "test"


@pytest.mark.django_db
def test_car_update_permission_denied(api_client, user, another_user, car):
    token = Token.objects.create(user=another_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = api_client.put(
        f"/api/cars/{car.id}/update/",
        {"make": "test", "model": "test", "year": 4321, "description": "test"},
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_car_delete_success(api_client, user, car):
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    car = Car.objects.create(
        make="test", model="Car 1", year=1234, owner=user, description="test"
    )
    response = api_client.delete(f"/api/cars/{car.id}/delete/")
    assert response.status_code == 204
