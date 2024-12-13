from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from cars.services import get_car_by_id
from core.loggers import apps_logger
from .forms import CommentForm
from .services import create_comment


@login_required
def add_comment(request, car_id: int):
    """Форма создания комментария."""
    car = get_car_by_id(car_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        apps_logger.debug(
            f"Пользователь с id {request.user.id} создал комментарий к автомобилю {car_id}."
        )
        create_comment(user=request.user, form=form, car=car)
    return redirect("cars:car_detail", car_id=car_id)
