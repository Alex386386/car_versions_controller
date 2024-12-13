import json

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from api.serializers import CarSerializer, CommentSerializer
from cars.models import Car, User


def list_cars() -> dict:
    """Получение из БД списка автомобилей."""
    cars = Car.objects.all()
    return CarSerializer(cars, many=True).data


def get_car_details(pk: int) -> dict:
    """Получение из БД конкретного автомобиля по id."""
    car = get_object_or_404(Car, pk=pk)
    return CarSerializer(car).data


def create_car(data, user) -> dict:
    """Создание автомобиля в БД."""
    serializer = CarSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(owner=user)
    return serializer.data


def _check_is_owner(car: Car, user: User) -> None:
    if car.owner != user:
        raise PermissionDenied("Вы не владелец этого автомобиля.")


def update_car(pk: int, data: json, user: User) -> dict:
    """Обновление автомобиля в БД."""
    car = get_object_or_404(Car, pk=pk)
    _check_is_owner(car=car, user=user)
    serializer = CarSerializer(car, data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data


def delete_car(pk: int, user: User) -> None:
    """Удаление автомобиля из БД по id."""
    car = get_object_or_404(Car, pk=pk)
    _check_is_owner(car=car, user=user)
    car.delete()


def list_car_comments(pk: int) -> dict:
    """Получение списка комментариев по объекту автомобиля."""
    car = get_object_or_404(Car, pk=pk)
    comments = car.comment_car.all()
    return CommentSerializer(comments, many=True).data


def add_car_comment(pk: int, data: json, user: User) -> dict:
    """Добавление комментария в БД."""
    car = get_object_or_404(Car, pk=pk)
    serializer = CommentSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(author=user, car=car)
    return serializer.data
