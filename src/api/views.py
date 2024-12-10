from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from cars.models import Car
from .serializers import CarSerializer, CommentSerializer


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def obtain_auth_token(request):
    """Получение токена для пользователя взаимодействующего по апи через пароль и юзернэйм."""
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    else:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def car_list(request):
    """
    Получение списка автомобилей.
    """
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def car_detail(request, pk):
    """
    Получение информации о конкретном автомобиле.
    """
    car = get_object_or_404(Car, pk=pk)
    serializer = CarSerializer(car)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def car_create(request):
    """
    Создание нового автомобиля.
    """
    serializer = CarSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def car_update(request, pk):
    """
    Обновление информации об автомобиле.
    """
    car = get_object_or_404(Car, pk=pk)
    if car.owner != request.user:
        return Response(
            {"detail": "Вы не владелец этого автомобиля."},
            status=status.HTTP_403_FORBIDDEN,
        )
    serializer = CarSerializer(car, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def car_delete(request, pk):
    """
    Удаление автомобиля.
    """
    car = get_object_or_404(Car, pk=pk)
    if car.owner != request.user:
        return Response(
            {"detail": "Вы не владелец этого автомобиля."},
            status=status.HTTP_403_FORBIDDEN,
        )
    car.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def car_comments_list(request, pk):
    """
    Получение комментариев к автомобилю.
    """
    car = get_object_or_404(Car, pk=pk)
    comments = car.comment_car.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def car_add_comment(request, pk):
    """
    Добавление нового комментария к автомобилю.
    """
    car = get_object_or_404(Car, pk=pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user, car=car)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
