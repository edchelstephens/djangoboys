from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    """User admin model."""

    fields = [
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "date_joined",
    ]


admin.site.register(User, UserAdmin)
