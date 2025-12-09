from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.create_user, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("delete_account/", views.delete_account, name="delete_account"),
]
