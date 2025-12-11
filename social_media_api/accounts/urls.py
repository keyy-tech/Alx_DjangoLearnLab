from django.urls import path
from .views import (
    ProfileView,
    RegisterView,
    LogoutView,
    AdminUsersView,
    FollowUserAPIView,
    UnFollowUserAPIView,
    LoginView,
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("admin/users/", AdminUsersView.as_view(), name="admin_users"),
    path("user/follow/<int:user_id>/", FollowUserAPIView.as_view(), name="follow_user"),
    path(
        "user/unfollow/<int:user_id>/",
        UnFollowUserAPIView.as_view(),
        name="unfollow_user",
    ),
]
