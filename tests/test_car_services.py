import pytest
from django.core.exceptions import PermissionDenied

from cars.forms import CarForm
from cars.services import (
    get_all_cars,
    get_car_by_id,
    create_car,
    create_comment,
    check_owner,
)
from comments.forms import CommentForm


@pytest.mark.django_db
def test_get_all_cars(car):
    """Тестирование получения всех автомобилей"""
    cars = get_all_cars()
    assert cars.count() == 1
    assert cars.first().make == "Toyota"


@pytest.mark.django_db
def test_get_car_by_id(car):
    """Тестирование получения автомобиля по id"""
    retrieved_car = get_car_by_id(car.id)
    assert retrieved_car == car


@pytest.mark.django_db
def test_create_car(user):
    """Тестирование создания автомобиля через сервис"""
    data = {
        "make": "Honda",
        "model": "Civic",
        "year": 2022,
        "description": "A new Honda Civic",
    }

    form = CarForm(data)
    created_car = create_car(form, user)
    assert created_car.make == "Honda"
    assert created_car.owner == user


@pytest.mark.django_db
def test_create_comment(user, car):
    """Тестирование создания комментария"""
    comment_data = {"content": "Great car!"}
    form = CommentForm(comment_data)
    create_comment(user, form, car)
    assert car.comment_car.count() == 1
    assert car.comment_car.first().content == "Great car!"


@pytest.mark.django_db
def test_check_owner(user, another_user, car):
    """Тестирование проверки владельца"""
    check_owner(user, car)

    with pytest.raises(PermissionDenied):
        check_owner(another_user, car)
