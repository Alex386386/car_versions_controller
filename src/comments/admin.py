from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "content",
        "car",
        "author",
    )
    empty_value_display = "-пусто-"
