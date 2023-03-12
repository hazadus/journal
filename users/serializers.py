from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model - full version.
    """
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "second_name",
            "last_name",
            "birthday",
            "avatar_img",
            "date_joined",
        ]


class CustomUserMinimalSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model - minimal version.
    """
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
        ]
