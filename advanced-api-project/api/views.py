from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import BookSerializer, AuthorSerializer
from .models import Book, Author
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["publication_year"]
    search_fields = [
        "title",
        "author__name",
    ]
    ordering_fields = [
        "-publication_year",
        "title",
    ]


class BookCreateView(generics.CreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookUpdateView(generics.UpdateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()


class BookDeleteView(generics.DestroyAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()


class BookDetailView(generics.RetrieveAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()
