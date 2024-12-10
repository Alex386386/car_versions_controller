from django.contrib.auth import get_user_model
from django.db import models

from core.models import Base

User = get_user_model()


class Car(Base):
    make = models.CharField(verbose_name="Марка автомобиля", max_length=100)
    model = models.CharField(verbose_name="Модель автомобиля", max_length=100)
    year = models.PositiveIntegerField(verbose_name="Год выпуска")
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(
        User, verbose_name="Владелец", on_delete=models.CASCADE, related_name="cars"
    )

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"
