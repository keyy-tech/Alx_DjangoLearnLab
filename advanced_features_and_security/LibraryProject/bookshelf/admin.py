from django.contrib import admin
from .models import Book, CustomUser


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "publication_year"]
    search_fields = ["title", "author"]
    list_filter = ["publication_year"]


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "last_login")
    fieldsets = (
        ("Credentials", {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


admin.site.register(CustomUser, CustomUserAdmin)
