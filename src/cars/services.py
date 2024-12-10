from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from comments.forms import CommentForm
from .forms import CarForm
from .models import Car, User
from .paginator import run_pagination


def _get_all_cars() -> QuerySet:
    """Получение всех объектов автомобилей для главной страницы."""
    return Car.objects.all().order_by("-id")


def get_car_by_id(car_id: int) -> Car:
    """Получение объекта автомобиля по id."""
    return get_object_or_404(Car, id=car_id)


def _get_comments_by_car(car: Car) -> QuerySet:
    """Получение комментариев через связную модель автомобиля."""
    return car.comment_car.all().order_by("-id")


def create_car(form: CarForm, user: User) -> Car:
    """Создание автомобиля через форму."""
    car = form.save(commit=False)
    car.owner = user
    car.save()
    return car


def create_comment(user: User, form: CommentForm, car: Car):
    """Создание комментария через форму"""
    comment = form.save(commit=False)
    comment.author = user
    comment.car = car
    comment.save()


def form_index_context(request: HttpRequest) -> dict:
    """Формирование контекста для главной страницы."""
    cars = _get_all_cars()
    page_obj = run_pagination(cars, request, 10)
    return {"page_obj": page_obj}


def form_detail_context(request: HttpRequest, car_id: int) -> dict:
    """Формирование контекста для страницы автомобиля."""
    car = get_car_by_id(car_id)
    comments = _get_comments_by_car(car)
    form = CommentForm(request.POST or None)
    return {
        "car": car,
        "comments": comments,
        "form": form,
    }


def _check_owner(request: HttpRequest, car: Car) -> None:
    """Проверка факта владения записью."""
    if car.owner != request.user:
        raise PermissionDenied("Вы не являетесь владельцем этого автомобиля.")


def get_car_and_check_owner(request: HttpRequest, car_id: int) -> Car:
    """Объединение функционала для вызова в контрольном слое."""
    car = get_car_by_id(car_id)
    _check_owner(request=request, car=car)
    return car
