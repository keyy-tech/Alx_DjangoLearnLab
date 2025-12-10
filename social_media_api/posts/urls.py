from django.urls import path
from . import views


urlpatterns = [
    path(
        "post/",
        views.PostListCreateView.as_view(),
        name="post-list-create",
    ),
    path(
        "post/<int:pk>/",
        views.PostRetrieveUpdateDestroyView.as_view(),
        name="post-retrieve-update-destroy",
    ),
    path("comment/", views.CommentCreateView.as_view(), name="comment-create"),
    path(
        "comment/<int:pk>/",
        views.CommentUpdateView.as_view(),
        name="comment-update-destroy",
    ),
]
