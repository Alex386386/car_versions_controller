from django.db import models


class Base(models.Model):
    """Базовый класс для создания моделей с датами обновления и создания объектов в БД."""

    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата обновления",
        auto_now=True,
    )

    class Meta:
        abstract = True
