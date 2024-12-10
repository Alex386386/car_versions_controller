from django.db import models

from cars.models import Car, User
from core.models import Base


class Comment(Base):
    content = models.TextField(verbose_name="Тело комментария")
    car = models.ForeignKey(
        Car,
        verbose_name="Автомобиль к которому относится комментарий",
        on_delete=models.CASCADE,
        related_name="comment_car",
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор комментария",
        on_delete=models.CASCADE,
        related_name="comment_author",
    )

    def __str__(self):
        return f"Comment by {self.author} on {self.car}"
