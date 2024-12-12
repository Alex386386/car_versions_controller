import pytest
from rest_framework.exceptions import PermissionDenied
from django.http.response import Http404
from src.api.services.car_service import (
    list_cars,
    get_car_details,
    create_car,
    update_car,
    delete_car,
    list_car_comments,
    add_car_comment,
)


@pytest.mark.django_db
def test_list_cars(car, car2):
    cars = list_cars()
    assert len(cars) == 2


@pytest.mark.django_db
def test_create_car(user):
    data = {"make": "test", "model": "Car 1", "year": 1234, "description": "test"}
    car_data = create_car(data, user)
    assert car_data["model"] == "Car 1"


@pytest.mark.django_db
def test_get_car(car):
    car_data = get_car_details(car.id)
    assert car_data["model"] == "Corolla"


@pytest.mark.django_db
def test_update_car_success(user, car):
    data = {"make": "test", "model": "test", "year": 4321, "description": "test"}
    updated_car = update_car(car.id, data, user)
    assert updated_car["model"] == "test"


@pytest.mark.django_db
def test_update_car_permission_denied(another_user, car):
    data = {"make": "test", "model": "test", "year": 4321, "description": "test"}
    with pytest.raises(PermissionDenied):
        update_car(car.id, data, another_user)


@pytest.mark.django_db
def test_delete_car_success(car, user):
    delete_car(car.id, user)
    with pytest.raises(Http404):
        get_car_details(car.id)


@pytest.mark.django_db
def test_add_car_comment(car, user):
    data = {"content": "Great car!"}
    comment_data = add_car_comment(car.id, data, user)
    assert comment_data["content"] == "Great car!"


@pytest.mark.django_db
def test_list_car_comment(car, comment, comment2):
    data = list_car_comments(car.id)
    assert len(data) == 2
