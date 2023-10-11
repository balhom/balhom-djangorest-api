from django.contrib import admin
from app_auth.models.user_model import User
from django.contrib.auth.models import Group

# Remove Groups from admin
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        "keycloak_id",
        "image",
        "last_login",
        "date_joined",
        (
            "is_superuser",
            "is_staff",
        ),
        (
            "is_active",
            "receive_email_balance",
        ),
        "count_pass_reset",
        (
            "current_balance",
            "pref_currency_type",
        ),
        (
            "expected_annual_balance",
            "expected_monthly_balance",
        ),
    )
    readonly_fields = (
        "keycloak_id",
        "last_login",
        "date_joined",
        "count_pass_reset",
        "current_balance",
    )
    list_display = (
        "last_login",
        "is_active",
    )
    list_filter = ("is_active",)
    ordering = ("last_login",)
