from rest_framework import status
from rest_framework.response import Response
from requests import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,CreateAPIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated


class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Post.objects.filter(author=self.request.user)
            .select_related("author")
            .prefetch_related("comments")
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = {
            "message": "Post created successfully",
            "data": response.data,
            "status": "success",
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        reponse = super().list(request, *args, **kwargs)
        data = {
            "message": "Posts retrieved successfully",
            "data": reponse.data,
            "status": "success",
        }
        return Response(data, status=status.HTTP_200_OK)


class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        data = {
            "message": "Post updated successfully",
            "data": response.data,
            "status": "success",
        }
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        data = {
            "message": "Post deleted successfully",
        }
        return Response(data, status=response.status_code)


class CommentCreateView(CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        

    def create(self,request,*args,**kwargs):
        response = super().create(request,*args,**kwargs)
        data = {
            "message": "Comment created successfully",
            "data": response.data,
            "status": "success",
        }
        return Response(data, status=status.HTTP_201_CREATED)


class CommentUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        data = {
            "message": "Comment updated successfully",
            "data": response.data,
            "status": "success",
        }
        return Response(data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        data = {
            "message": "Comment deleted successfully"
        }
        return Response(data, status=response.status_code)    


