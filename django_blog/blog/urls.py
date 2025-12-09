from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # -------------------------
    # USER AUTH
    # -------------------------
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # PROFILE
    path("profile/", views.profile_view, name="profile"),
    path("profile/update/", views.update_profile, name="update-profile"),
    path("profile/delete/", views.delete_account, name="delete-account"),
    # -------------------------
    # POSTS
    # -------------------------
    path("", views.PostListView.as_view(), name="post-list"),
    path("post/create/", views.PostCreateView.as_view(), name="post-create"),
    path(
        "post/<int:pk>/", views.PostUpdateView.as_view(), name="post-detail"
    ),  # if you want a detail view, add later
    path("post/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    # -------------------------
    # COMMENTS
    # -------------------------
    path(
        "post/<int:pk>/comments/new/",
        views.CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "comment/<int:pk>/update/",
        views.CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "comment/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="comment-delete",
    ),
    path("comment/", views.CommentListView.as_view(), name="comment-list"),
]
