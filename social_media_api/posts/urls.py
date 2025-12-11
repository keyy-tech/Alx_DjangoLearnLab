from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"posts", views.PostViewSet)
router.register(r"comments", views.CommentViewSet)


urlpatterns = [
    path("feed/",views.UserFeedView.as_view(),name="user-feed")
] + router.urls
