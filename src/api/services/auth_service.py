from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token


def get_user_token(username: str, password: str):
    """Получение объекта токена."""
    user = authenticate(username=username, password=password)
    if user is None:
        raise AuthenticationFailed("Invalid credentials")
    token, _ = Token.objects.get_or_create(user=user)
    return token.key
