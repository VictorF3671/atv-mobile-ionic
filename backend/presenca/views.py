# presenca/views.py
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Presenca
from .serializers import (
    UserListSerializer,
    UserCreateUpdateSerializer,
    PresencaSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de usuários:
    - GET /api/usuarios/        -> lista
    - POST /api/usuarios/       -> cria
    - GET /api/usuarios/{id}/   -> detalhe
    - PUT /api/usuarios/{id}/   -> atualiza tudo
    - PATCH /api/usuarios/{id}/ -> atualiza parcial
    - DELETE /api/usuarios/{id}/ -> exclui
    """

    queryset = User.objects.all().order_by("id")
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return UserListSerializer
        return UserCreateUpdateSerializer

    @swagger_auto_schema(
        operation_description="Cria um novo usuário.",
        request_body=UserCreateUpdateSerializer,
        responses={201: UserListSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Atualiza completamente um usuário (PUT).",
        request_body=UserCreateUpdateSerializer,
        responses={200: UserListSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Atualiza parcialmente um usuário (PATCH).",
        request_body=UserCreateUpdateSerializer,
        responses={200: UserListSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class PresencaViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de presenças:
    - GET /api/presencas/
    - POST /api/presencas/
    - GET /api/presencas/{id}/
    - PUT /api/presencas/{id}/
    - PATCH /api/presencas/{id}/
    - DELETE /api/presencas/{id}/
    """

    queryset = Presenca.objects.select_related("user").all().order_by("-data", "-criado_em")
    serializer_class = PresencaSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description=(
            "Cria uma presença.\n\n"
            "Body exemplo:\n"
            "{\n"
            '  "user": 1,\n'
            '  "data": "2025-12-04"\n'
            "}\n\n"
            "Regra: não permite duas presenças para o mesmo usuário na mesma data."
        ),
        request_body=PresencaSerializer,
        responses={201: PresencaSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            "Atualiza uma presença (por exemplo, corrigir a data)."
        ),
        request_body=PresencaSerializer,
        responses={200: PresencaSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Atualiza parcialmente uma presença.",
        request_body=PresencaSerializer,
        responses={200: PresencaSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class LoginView(APIView):
    """
    Login simples só para validar usuário/senha.

    POST /api/login/
    {
      "username": "victor",
      "password": "1234"
    }
    """

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Realiza login simples (sem token), apenas valida usuário e senha.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, example="victor"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, example="1234"
                ),
            },
            required=["username", "password"],
        ),
        responses={
            200: openapi.Response(
                description="Login bem-sucedido",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, example="Login realizado com sucesso!"
                        ),
                        "user_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        "username": openapi.Schema(type=openapi.TYPE_STRING, example="victor"),
                    },
                ),
            ),
            400: openapi.Response(
                description="Credenciais inválidas ou dados faltando",
            ),
        },
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Informe username e password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"error": "Credenciais inválidas."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Login realizado com sucesso!",
                "user_id": user.id,
                "username": user.username,
            },
            status=status.HTTP_200_OK,
        )
