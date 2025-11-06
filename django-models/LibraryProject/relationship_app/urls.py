from django.urls import path
from .views import  DetailLibraryView
from .views import list_books

urlpatterns = [
    path("books/", list_books, name="list_all_books"),
    path("library/<int:pk>/", DetailLibraryView.as_view(), name="detail_book_list"),
]
