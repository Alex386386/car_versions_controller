from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from core.loggers import api_logger
from .services import auth_service, car_service


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def obtain_auth_token(request):
    """Получение токена для пользователя."""
    username = request.data.get("username")
    password = request.data.get("password")
    try:
        token = auth_service.get_user_token(username, password)
        api_logger.debug("Токен успешно сформирован.")
        return Response({"token": token})
    except Exception as e:
        api_logger.debug(f"Ошибка: {e}")
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def car_list(request):
    """Получение списка автомобилей."""
    data = car_service.list_cars()
    api_logger.debug("Получены все объекты автомобилей.")
    return Response(data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def car_detail(request, pk):
    """Получение информации о конкретном автомобиле."""
    data = car_service.get_car_details(pk)
    api_logger.debug(f"Получены автомобиль с id {pk}.")
    return Response(data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def car_create(request):
    """Создание нового автомобиля."""
    data = car_service.create_car(request.data, request.user)
    api_logger.debug(f"Пользователь с id {request.user.id}.")
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def car_update(request, pk):
    """Обновление информации об автомобиле."""
    try:
        data = car_service.update_car(pk, request.data, request.user)
        api_logger.debug(
            f"Пользователь с id {request.user.id} обновил автомобиль {pk}."
        )
        return Response(data)
    except PermissionDenied as e:
        api_logger.error(
            f"Пользователь с id {request.user.id} пытался удалить автомобиль не принадлежащий ему."
        )
        return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def car_delete(request, pk):
    """Удаление автомобиля."""
    try:
        car_service.delete_car(pk, request.user)
        api_logger.debug(f"Пользователь с id {request.user.id} удалил автомобиль {pk}.")
        return Response(status=status.HTTP_204_NO_CONTENT)
    except PermissionDenied as e:
        api_logger.error(
            f"Пользователь с id {request.user.id} пытался удалить автомобиль не принадлежащий ему."
        )
        return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def car_comments_list(request, pk):
    """Получение комментариев к автомобилю."""
    data = car_service.list_car_comments(pk)
    api_logger.debug(f"Получен список комментариев для автомобиля {pk}.")
    return Response(data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def car_add_comment(request, pk):
    """Добавление нового комментария к автомобилю."""
    data = car_service.add_car_comment(pk, request.data, request.user)
    api_logger.debug(
        f"Пользователь с id {request.user.id} добавил комментарий к автомобилю {pk}."
    )
    return Response(data, status=status.HTTP_201_CREATED)
