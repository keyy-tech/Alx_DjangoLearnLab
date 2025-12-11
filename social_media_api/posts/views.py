from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
