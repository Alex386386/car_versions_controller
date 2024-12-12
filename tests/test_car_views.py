import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from cars.models import Car
from django.test import Client
from pytest_django.asserts import assertContains


@pytest.mark.django_db
def test_index(client, car):
    """Тестирование главной страницы"""
    url = reverse("cars:index")
    response = client.get(url)
    assert response.status_code == 200
    assertContains(response, "Toyota")


@pytest.mark.django_db
def test_car_detail(client, car):
    """Тестирование страницы автомобиля"""
    url = reverse("cars:car_detail", args=[car.id])
    response = client.get(url)
    assert response.status_code == 200
    assertContains(response, car.make)
    assertContains(response, car.model)


@pytest.mark.django_db
def test_car_create(client, user):
    """Тестирование создания автомобиля"""
    client.login(username="testuser", password="testpassword")
    url = reverse("cars:car_create")
    data = {
        "make": "Honda",
        "model": "Civic",
        "year": 2022,
        "description": "A new Honda Civic",
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Ожидаем редирект на главную страницу
    assert Car.objects.filter(make="Honda", model="Civic").exists()


@pytest.mark.django_db
def test_update_car(client, user, car):
    """Тестирование обновления автомобиля"""
    client.login(username="testuser", password="testpassword")
    url = reverse("cars:car_update", args=[car.id])
    data = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2021,
        "description": "Updated car",
    }
    response = client.post(url, data)
    assert response.status_code == 302
    car.refresh_from_db()
    assert car.model == "Camry"
    assert car.year == 2021


@pytest.mark.django_db
def test_update_car_permission_denied(client, user, another_user, car):
    """Тестирование ошибки доступа при попытке обновить чужой автомобиль"""
    client.login(username="testuser2", password="testpassword2")
    data = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2021,
        "description": "Updated car",
    }
    url = reverse("cars:car_update", args=[car.id])
    response = client.post(url, data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_check_owner(client, user, another_user, car):
    """Тестирование проверки владельца автомобиля"""
    data = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2021,
        "description": "Updated car",
    }
    client.login(username="testuser", password="testpassword")

    url = reverse("cars:car_update", args=[car.id])
    response = client.post(url, data)
    assert response.status_code == 302

    client.login(username="testuser2", password="testpassword2")
    response = client.post(url, data)
    assert response.status_code == 403
