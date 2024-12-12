import pytest

from django.contrib.auth.models import User
from django.test import Client

from rest_framework.test import APIClient


@pytest.fixture
def user():
    """Создание тестового пользователя"""
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def another_user():
    """Создание тестового пользователя"""
    return User.objects.create_user(username="testuser2", password="testpassword2")


@pytest.fixture
def client():
    """Возвращает клиент для тестирования"""
    return Client()


@pytest.fixture
def api_client():
    """Возвращает клиент для тестирования"""
    return APIClient()
