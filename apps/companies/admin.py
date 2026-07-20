from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "trade_name",
        "owner",
        "max_users",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "trade_name",
        "document",
        "email",
        "owner__email",
    )

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )

    fieldsets = (
        ("Identificação", {
            "fields": (
                "name",
                "trade_name",
                "slug",
                "document",
            ),
        }),

        ("Contato", {
            "fields": (
                "email",
                "phone",
            ),
        }),

        ("Responsável", {
            "fields": (
                "owner",
            ),
        }),

        ("Configuração da conta", {
            "fields": (
                "max_users",
                "is_active",
            ),
        }),

        ("Datas", {
            "fields": (
                "created_at",
                "updated_at",
            ),
        }),
    )