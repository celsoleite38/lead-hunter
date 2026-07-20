from django.conf import settings
from django.db import models
from django.utils.text import slugify
from validate_docbr import CPF, CNPJ
from django.core.exceptions import ValidationError

def validate_cpf_cnpj(value):
    # Remove pontos, traços e barras para validar apenas os números
    clean_value = "".join(filter(str.isdigit, value))
    
    # Verifica o tamanho do dado limpo
    if len(clean_value) == 11:
        if not CPF().validate(clean_value):
            raise ValidationError("CPF inválido.")
    elif len(clean_value) == 14:
        if not CNPJ().validate(clean_value):
            raise ValidationError("CNPJ inválido.")
    else:
        raise ValidationError("O documento deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ).")

class Company(models.Model):
    """
    Empresa cliente da plataforma Lead Hunter.
    """

    name = models.CharField(
        "Razão social ou nome da empresa",
        max_length=150,
    )

    trade_name = models.CharField(
        "Nome fantasia",
        max_length=150,
        blank=True,
    )

    slug = models.SlugField(
        "Identificador",
        max_length=170,
        unique=True,
        blank=True,
    )

    document = models.CharField(
        "CPF ou CNPJ",
        max_length=18,
        unique=True,
        blank=True,
        null=True,
        validators=[validate_cpf_cnpj]
    )

    email = models.EmailField(
        "E-mail da empresa",
        blank=True,
    )

    phone = models.CharField(
        "Telefone",
        max_length=20,
        blank=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Proprietário",
        related_name="owned_companies",
        on_delete=models.PROTECT,
    )

    max_users = models.PositiveIntegerField(
        "Limite de usuários",
        default=2,
    )

    is_active = models.BooleanField(
        "Empresa ativa",
        default=True,
    )

    created_at = models.DateTimeField(
        "Criada em",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Atualizada em",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["name"]

    def __str__(self):
        return self.trade_name or self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()

        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        base_slug = slugify(self.trade_name or self.name) or "empresa"
        slug = base_slug
        counter = 2

        while Company.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug