from django.contrib import admin
from .models import Book, Author, Library, Librarian, CustomUser

admin.site.site_header = "Library Management Admin"
admin.site.site_title = "Library Management Admin Portal"
admin.site.index_title = "Welcome to Library Management Admin Portal"


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author")


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ("name", "library")


@admin.register(CustomUser)
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
