# presenca/serializers/user_serializer.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    """Usado para listar e detalhar usuários (sem senha)."""

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "is_active")


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    """Usado para criar/atualizar usuário (com senha no body)."""

    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "password")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
