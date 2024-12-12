from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from api.serializers import CarSerializer, CommentSerializer
from cars.models import Car


def list_cars():
    """Получение из БД списка автомобилей."""
    cars = Car.objects.all()
    return CarSerializer(cars, many=True).data


def get_car_details(pk: int):
    """Получение из БД конкретного автомобиля по id."""
    car = get_object_or_404(Car, pk=pk)
    return CarSerializer(car).data


def create_car(data, user):
    """Создание автомобиля в БД."""
    serializer = CarSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(owner=user)
    return serializer.data


def update_car(pk: int, data, user):
    """Обновление автомобиля в БД."""
    car = get_object_or_404(Car, pk=pk)
    if car.owner != user:
        raise PermissionDenied("Вы не владелец этого автомобиля.")
    serializer = CarSerializer(car, data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data


def delete_car(pk: int, user):
    """Удаление автомобиля из БД по id."""
    car = get_object_or_404(Car, pk=pk)
    if car.owner != user:
        raise PermissionDenied("Вы не владелец этого автомобиля.")
    car.delete()


def list_car_comments(pk: int):
    """Получение списка комментариев по объекту автомобиля."""
    car = get_object_or_404(Car, pk=pk)
    comments = car.comment_car.all()
    return CommentSerializer(comments, many=True).data


def add_car_comment(pk: int, data, user):
    """Добавление комментария в БД."""
    car = get_object_or_404(Car, pk=pk)
    serializer = CommentSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(author=user, car=car)
    return serializer.data
