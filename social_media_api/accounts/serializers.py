from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token

User = get_user_model()


class AccountsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "bio",
            "profile_picture",
            "password",
            "password1",
        ]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate(self, data):
        if data["password"] != data["password1"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        validated_data.pop("password1")
        user = User.objects.create_user(**validated_data)  
        Token.objects.create(user=user)  
        return user
