from django.urls import path


from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"posts", views.PostViewSet)
router.register(r"comments", views.CommentViewSet)


urlpatterns = [
    path("feed/", views.UserFeedView.as_view(), name="user-feed"),
    path("<int:pk>/like/", views.UserLikePostView.as_view(), name="like-post"),
    path("<int:pk>/unlike/", views.UserUnlikePostView.as_view(), name="unlike-post"),
]


urlpatterns += router.urls
