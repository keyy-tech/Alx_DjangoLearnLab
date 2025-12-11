from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from .serializers import AccountsSerializer
from rest_framework.generics import CreateAPIView
from .models import Accounts as CustomUser
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.views import ObtainAuthToken


@extend_schema(tags=["Authentication & Authorisation"])
class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AccountsSerializer
    permission_classes = [permissions.AllowAny]
    models = CustomUser


@extend_schema(request=None, responses=None, tags=["Authentication & Authorisation"])
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = get_object_or_404(Token, user=request.user)
        token.delete()
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )


@extend_schema(tags=["Authentication & Authorisation"])
class LoginView(ObtainAuthToken):
    """Custom login view with schema support."""

    pass


@extend_schema(request=None, responses=None, tags=["Authentication & Authorisation"])
class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        serializer = AccountsSerializer(request.user)
        response = {
            "status": "success",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


@extend_schema(request=None, responses=None, tags=["Authentication & Authorisation"])
class AdminUsersView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request: Request):
        users = CustomUser.objects.all()
        serializer = AccountsSerializer(users, many=True)
        response = {
            "status": "success",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


@extend_schema(request=None, responses=None, tags=["Followers System"])
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

        data = {"message": f"You are now following {user_to_follow.username}"}

        return Response(data, status=status.HTTP_200_OK)


@extend_schema(request=None, responses=None, tags=["Followers System"])
class UnFollowUserAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, user_id, *args, **kwargs):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user
        if user_to_unfollow == current_user:
            return Response(
                {"detail": "You can't unfollow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_to_unfollow.followers.remove(current_user)

        data = {"message": f"You have unfollowed {user_to_unfollow.username}"}
        return Response(data, status=status.HTTP_200_OK)
