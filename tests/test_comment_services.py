import pytest
from comments.models import Comment
from cars.services import create_comment
from comments.forms import CommentForm


@pytest.mark.django_db
def test_create_comment(user, car):
    """Тестирование создания комментария через сервис."""

    data = {"content": "This is a test comment."}
    form = CommentForm(data=data)

    assert form.is_valid()

    create_comment(user=user, form=form, car=car)

    comment = Comment.objects.first()
    assert comment.content == "This is a test comment."
    assert comment.author == user
    assert comment.car == car


@pytest.mark.django_db
def test_create_comment_with_invalid_data(user, car):
    """Тестирование создания комментария через сервис с невалидными данными."""

    form = CommentForm(data={"content": ""})

    assert not form.is_valid()

    with pytest.raises(ValueError):
        create_comment(user=user, form=form, car=car)
