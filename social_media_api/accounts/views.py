from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post
from posts.serializers import PostSerializer
from .serializers import AccountsSerializer
from rest_framework.generics import CreateAPIView
from .models import Accounts as CustomUser
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework import generics



class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AccountsSerializer
    permission_classes = [permissions.AllowAny]
    models = CustomUser


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request):
        token = get_object_or_404(Token, user=request.user)
        token.delete()
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        serializer = AccountsSerializer(request.user)
        response = {
            "status": "success",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


class AdminUsersView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request: Request):
        users = CustomUser.objects.all()
        serializer = AccountsSerializer(users, many=True)
        response = {
            "status": "success",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


class FollowUserAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, user_id: int):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user
        if user_to_follow == current_user:
            return Response(
                {"detail": "You can't follow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_to_follow.followers.add(current_user)

        data = {
            "message": f"You are now following {user_to_follow.username}"
        }

        return Response(data,status=status.HTTP_200_OK)


class UnFollowUserAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request:Request,user_id,*args,**kwargs):
        user_to_unfollow = get_object_or_404(CustomUser,id=user_id)
        current_user = request.user
        if user_to_unfollow == current_user:
            return Response(
                {"detail":"You can't unfollow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_to_unfollow.followers.remove(current_user)

        data = {
            "message":f"You have unfollowed {user_to_unfollow.username}"
        }
        return Response(data,status=status.HTTP_200_OK)


class UserFeed(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request:Request,*args,**kwargs):
        following_users = request.user.following.all()

        feed_posts = Post.objects.filter(author__in=following_users).order_by("-created_at")

        serializer = PostSerializer(feed_posts,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
