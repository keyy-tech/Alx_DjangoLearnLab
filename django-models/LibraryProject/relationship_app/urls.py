from django.urls import path
from .views import list_all_books, DetailLibraryView

urlpatterns = [
    path("books/", list_all_books, name="list_all_books"),
    path("library/<int:pk>/", DetailLibraryView.as_view(), name="detail_book_list"),
]
