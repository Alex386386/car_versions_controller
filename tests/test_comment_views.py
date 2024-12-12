import pytest
from django.urls import reverse

from comments.models import Comment


@pytest.mark.django_db
def test_add_comment_view(client, user, car):
    """Тестирование добавления комментария через представление."""

    client.login(username=user.username, password="testpassword")

    url = reverse("comments:add_comment", args=[car.id])
    comment_content = "This is a test comment."
    response = client.post(url, {"content": comment_content})

    assert Comment.objects.count() == 1
    comment = Comment.objects.first()
    assert comment.content == comment_content
    assert comment.author == user
    assert comment.car == car

    assert response.status_code == 302
    assert response.url == reverse("cars:car_detail", args=[car.id])


@pytest.mark.django_db
def test_add_comment_view_without_login(client, car):
    """Тестирование того, что добавление комментария без авторизации приводит к редиректу на страницу логина."""

    url = reverse("comments:add_comment", args=[car.id])
    response = client.get(url)

    assert response.status_code == 302
