from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page

from core.loggers import apps_logger
from .forms import CarForm
from .services import (
    form_index_context,
    form_detail_context,
    create_car,
    get_car_and_check_owner,
)


@cache_page(10, key_prefix="index_page")
def index(request: HttpRequest) -> HttpResponse:
    """Главная страница."""
    context = form_index_context(request=request)
    apps_logger.debug("Контекст главной страницы получен")
    return render(request, "cars/index.html", context)


def car_detail(request: HttpRequest, car_id: int) -> HttpResponse:
    """Страница автомобиля полученного по id."""
    context = form_detail_context(request=request, car_id=car_id)
    apps_logger.debug(f"Контекст страницы автомобиля с id {car_id}")
    return render(request, "cars/car_detail.html", context)


@login_required
def car_create(request: HttpRequest) -> HttpResponse:
    """Форма создания автомобиля"""
    form = CarForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        create_car(form=form, user=request.user)
        apps_logger.debug(f"Пользователь с id {request.user.id} создал автомобиль")
        return redirect("cars:index")
    context = {"form": form}
    return render(request, "cars/create_car.html", context)


@login_required
def update_car(request: HttpRequest, car_id: int) -> HttpResponse:
    """Форма обновления автомобиля."""
    car = get_car_and_check_owner(request=request, car_id=car_id)

    if request.method == "POST":
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            apps_logger.debug(
                f"Пользователь с id {request.user.id} обновил автомобиль {car_id}."
            )
            return redirect("cars:car_detail", car_id=car.id)
    else:
        form = CarForm(instance=car)

    context = {
        "form": form,
        "car": car,
    }
    return render(request, "cars/update_car.html", context)
