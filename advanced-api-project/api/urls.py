from django.urls import path
from .views import (
    BookListView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/create/", BookCreateView.as_view(), name="book-create"),
    path("books/update/<int:pk>/", BookUpdateView.as_view(), name="book-update"),
    path("books/delete/<int:pk>/", BookDeleteView.as_view(), name="book-delete"),
    path("token/create/", obtain_auth_token, name="token_obtain_pair"),
]
