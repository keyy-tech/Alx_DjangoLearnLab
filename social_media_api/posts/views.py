from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions
from .models import Post, Comment,Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def get_queryset(self):
        # Only return posts authored by the logged-in user
        return (
            Post.objects.filter(author=self.request.user)
            .select_related("author")  # fetch author in same query
            .prefetch_related("comments__author")  # prefetch comments and their authors
        )

    def perform_create(self, serializer):
        # Set the author to the logged-in user
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "message": "Post created successfully",
                "data": response.data,
                "status": "success",
            },
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "message": "Posts retrieved successfully",
                "data": response.data,
                "status": "success",
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {
                "message": "Post updated successfully",
                "data": response.data,
                "status": "success",
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "Post deleted successfully"}, status=status.HTTP_200_OK
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()

    def get_queryset(self):
        # Only return comments authored by the logged-in user
        return Comment.objects.filter(author=self.request.user).select_related(
            "author", "post"
        )  # fetch author and related post

    def perform_create(self, serializer):
        # Set the author to the logged-in user
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "message": "Comment created successfully",
                "data": response.data,
                "status": "success",
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {
                "message": "Comment updated successfully",
                "data": response.data,
                "status": "success",
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "Comment deleted successfully"}, status=status.HTTP_200_OK
        )


class UserFeedView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        following_users = request.user.following.all()

        feed_posts = Post.objects.filter(author__in=following_users).order_by("-created_at")

        serializer = PostSerializer(feed_posts,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


class UserLikePostView(generics.GenericAPIView):
    permissions_classes = [permissions.IsAuthenticated]

    def post(self,request,pk,*args,**kwargs):
        post = get_object_or_404(Post,id=pk)
        current_user = request.user

        # create the like
        if Like.objects.filter(user=current_user,post=post).exists():
            return Response(
                {"detail":"You can't double the like a post"},
                status=status.HTTP_400_BAD_REQUEST
            )

        like = Like.objects.create(user=current_user,post=post)
        like.save()

        return Response(
            {"detail":f"You have successfully liked the post with title - {post.title} by {post.author.get_full_name()}."}
        )



class UserUnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,pk,*args,**kwargs):
        post = get_object_or_404(Post,id=pk)
        current_user = request.user

        like = Like.objects.filter(user=current_user,post=post).first()
        if not like:
            return Response(
                {"detail":"You have not liked this post"},
                status=status.HTTP_400_BAD_REQUEST
            )

        like.delete()

        return Response(
            {"detail":f"You have unliked the post '{post.title}'"},
            status=status.HTTP_200_OK
        )

