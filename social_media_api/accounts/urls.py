from django.urls import path
from .views import ProfileView, RegisterView, LogoutView,AdminUsersView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", obtain_auth_token, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("admin/users/", AdminUsersView.as_view(), name="admin_users"),
]
