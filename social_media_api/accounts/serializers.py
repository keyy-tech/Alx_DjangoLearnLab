from rest_framework import serializers
from .models import Accounts
from django.contrib.auth.password_validation import validate_password


class AccountsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = Accounts
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
        if Accounts.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if Accounts.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate(self, data):
        # Cross-field validation for passwords
        if data["password"] != data["password1"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        # Validate password strength using Django validators
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        # Remove password1 before creating user
        validated_data.pop("password1")
        return Accounts.objects.create_user(**validated_data)
    

