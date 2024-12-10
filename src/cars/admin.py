from django.contrib import admin

from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "make",
        "year",
        "description",
        "owner",
    )
    empty_value_display = "-пусто-"
