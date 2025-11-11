from django.contrib import admin
from .models import Book, Author, Library, Librarian

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
