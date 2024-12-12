import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from src.api.services.auth_service import get_user_token


@pytest.mark.django_db
def test_get_user_token_success():
    user = User.objects.create_user(username="testuser", password="password")
    token = get_user_token("testuser", "password")
    assert token == Token.objects.get(user=user).key


@pytest.mark.django_db
def test_get_user_token_invalid_credentials():
    User.objects.create_user(username="testuser", password="password")
    with pytest.raises(AuthenticationFailed):
        get_user_token("testuser", "wrongpassword")
