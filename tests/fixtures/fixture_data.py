import pytest

from cars.models import Car
from comments.models import Comment


@pytest.fixture
def car(user):
    """Создание тестового автомобиля для пользователя"""
    return Car.objects.create(
        make="Toyota", model="Corolla", year=2020, description="Test car", owner=user
    )


@pytest.fixture
def car2(user):
    """Создание тестового автомобиля для пользователя"""
    return Car.objects.create(
        make="Lada", model="Priora", year=2022, description="Test car", owner=user
    )


@pytest.fixture
def comment(user, car):
    return Comment.objects.create(content="test", author=user, car=car)


@pytest.fixture
def comment2(user, car):
    return Comment.objects.create(content="test2", author=user, car=car)
