# presenca/serializers/presenca_serializer.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from presenca.models import Presenca

User = get_user_model()


class PresencaSerializer(serializers.ModelSerializer):
    """
    CRUD completo de Presença.
    Já mostra o username no retorno.
    """

    user_username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Presenca
        fields = ("id", "user", "user_username", "data", "criado_em")
        read_only_fields = ("criado_em",)

    def validate(self, attrs):
        """
        Garante que não exista mais de uma presença
        para o mesmo usuário na mesma data.
        """
        user = attrs.get("user") or getattr(self.instance, "user", None)
        data = attrs.get("data") or getattr(self.instance, "data", None)

        if not user or not data:
            return attrs

        qs = Presenca.objects.filter(user=user, data=data)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "Já existe presença para este usuário nessa data."
            )

        return attrs
