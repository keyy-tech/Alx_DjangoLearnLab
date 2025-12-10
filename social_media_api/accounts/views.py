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
