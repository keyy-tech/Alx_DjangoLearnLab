from django.urls import path
from .views import LibraryDetailView
from .views import list_books

urlpatterns = [
    path("books/", list_books, name="list_all_books"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="detail_book_list"),
]
