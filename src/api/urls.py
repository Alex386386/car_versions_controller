from django.urls import path

from .views import (
    car_list,
    car_detail,
    car_create,
    car_update,
    car_delete,
    car_comments_list,
    car_add_comment,
    obtain_auth_token,
)

urlpatterns = [
    path("token/", obtain_auth_token, name="api_token"),
    path("cars/", car_list, name="car_list"),
    path("cars/<int:pk>/", car_detail, name="car_detail"),
    path("cars/create/", car_create, name="car_create"),
    path("cars/<int:pk>/update/", car_update, name="car_update"),
    path("cars/<int:pk>/delete/", car_delete, name="car_delete"),
    path("cars/<int:pk>/comments/", car_comments_list, name="car_comments_list"),
    path("cars/<int:pk>/comments/add/", car_add_comment, name="car_add_comment"),
]
