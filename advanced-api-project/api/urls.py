from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("book/", views.BookListView.as_view(), name="book_list"),
    path("book/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("book/<int:pk>/update/", views.BookUpdateView.as_view(), name="book_update"),
    path("book/<int:pk>/delete/", views.BookDeleteView.as_view(), name="book_delete"),
    path("book/create/", views.BookCreateView.as_view(), name="book_create"),
    path("token/create/", obtain_auth_token, name="token_obtain_pair"),
]
