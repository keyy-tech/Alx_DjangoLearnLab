from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status

from api.models import Author, Book


class APITesting(APITestCase):
    def setUp(self):
        # create a user once per test
        self.user = User.objects.create_user(username="keyytech", password="keyy@123")

        # create an author instance
        self.author = Author.objects.create(name="Emmanuel Kotoka")

        # create a book instance
        self.book = Book.objects.create(
            title="Life Book 1",
            publication_year=2021,
            author=self.author,
        )

        # create the client
        self.client = APIClient()

        # avoid duplicate tokens across test runs
        self.token, _ = Token.objects.get_or_create(user=self.user)

        # attach token to client for authenticated requests
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_create_book(self):
        self.url = reverse("book-create")

        self.data = {
            "title": "Life Book 1",
            "publication_year": 2021,
            "author": self.author.id,
        }

        response = self.client.post(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthorized_create_book(self):
        self.url = reverse("book-create")

        self.data = {
            "title": "Life Book 1",
            "publication_year": 2023,
            "author": self.author.id,
        }

        self.client = APIClient()

        response = self.client.post(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_book(self):
        self.url = reverse("book-update", kwargs={"pk": self.book.id})

        self.data = {"title": "Life Book 2", "publication_year": 2025}

        response = self.client.patch(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_update_book(self):
        self.url = reverse("book-update", kwargs={"pk": self.book.id})

        self.data = {
            "title": "Life Book",
            "publication_year": 2023,
            "author": self.author.id,
        }

        response = self.client.put(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_list(self):
        self.url = reverse("book-list")

        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        self.url = reverse("book-delete", kwargs={"pk": self.book.id})

        response = self.client.delete(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Book.objects.filter(pk=self.book.id).exists())

    def test_search_book(self):
        self.url = reverse("book-list") + f"?search=Book"

        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorised_book_list(self):
        self.url = reverse("book-list")

        self.client = APIClient()

        response = self.client.get(self.url, format="json")

        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
