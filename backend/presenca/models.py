from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    pass


class Presenca(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="presencas",
    )
    data = models.DateField(auto_now_add=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Presença"
        verbose_name_plural = "Presenças"
        unique_together = ("user", "data")

    def __str__(self):
        return f"{self.user.username} - {self.data}"
