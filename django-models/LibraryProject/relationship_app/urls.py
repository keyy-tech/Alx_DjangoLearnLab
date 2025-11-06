from django.urls import path
from .views import LibraryDetailView
from .views import list_books
from django.contrib.auth import views as auth_views
from .views import UserRegisterView

urlpatterns = [
    path("books/", list_books, name="list_all_books"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="detail_book_list"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="relationship_app/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="relationship_app/logout.html"),
        name="logout",
    ),
    path("register/", UserRegisterView.as_view(), name="register"),
]
