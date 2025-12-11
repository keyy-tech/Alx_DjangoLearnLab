from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AccountsSerializer
from rest_framework.generics import CreateAPIView
from .models import Accounts
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404


class RegisterView(CreateAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    permission_classes = [AllowAny]
    models = Accounts


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        token = get_object_or_404(Token, user=request.user)
        token.delete()
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        serializer = AccountsSerializer(request.user)
        response = {
            "status": "success",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


class AdminUsersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request):
        users = Accounts.objects.all()
        serializer = AccountsSerializer(users, many=True)
        response = {
            "status": "success",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


class FollowUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, user_id: int):
        user_to_follow = get_object_or_404(Accounts, id=user_id)
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


class UnFollowUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request:Request,user_id:int):
        user_to_unfollow = get_object_or_404(Accounts,id=user_id)
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


