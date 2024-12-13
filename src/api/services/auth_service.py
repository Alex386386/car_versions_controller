from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from core.loggers import api_logger


def get_user_token(username: str, password: str):
    """Получение объекта токена."""
    user = authenticate(username=username, password=password)
    if user is None:
        api_logger.error("Произошла попытка получения токена с неправильными данными.")
        raise AuthenticationFailed("Invalid credentials")
    token, _ = Token.objects.get_or_create(user=user)
    return token.key
