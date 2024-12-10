from rest_framework import serializers

from cars.models import Car, User
from comments.models import Comment


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
        )


class CarSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ("id", "make", "model", "year", "description", "owner")


class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    car = CarSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "car",
            "author",
        )
