from django.utils import timezone
from rest_framework import serializers
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "publication_year", "author", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]

    def validate_publication_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future"
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["name", "books", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]
