from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager


class User(AbstractUser):
    """
    Usuário da plataforma InnoSoft.
    Autenticação realizada por e-mail.
    """

    username = None

    email = models.EmailField(
        "E-mail",
        unique=True
    )

    first_name = models.CharField(
        "Nome",
        max_length=80
    )

    last_name = models.CharField(
        "Sobrenome",
        max_length=120,
        blank=True
    )

    phone = models.CharField(
        "Telefone",
        max_length=20,
        blank=True
    )

    avatar = models.ImageField(
        "Foto",
        upload_to="avatars/",
        blank=True,
        null=True
    )

    company = models.ForeignKey(
        "companies.Company",
        verbose_name="Empresa",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    is_owner = models.BooleanField(
        "Proprietário da Empresa",
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["first_name"]

    def __str__(self):
        nome = f"{self.first_name} {self.last_name}".strip()
        return nome if nome else self.email