from cars.models import User, Car
from .forms import CommentForm


def create_comment(user: User, form: CommentForm, car: Car):
    """Создание комментария."""
    comment = form.save(commit=False)
    comment.author = user
    comment.car = car
    comment.save()
