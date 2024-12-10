from django.urls import path

from . import views

app_name = "cars"

urlpatterns = [
    path("", views.index, name="index"),
    path("car/detail/<int:car_id>/", views.car_detail, name="car_detail"),
    path("car/create/", views.car_create, name="car_create"),
    path("car/update/<int:car_id>/", views.update_car, name="car_update"),
]
