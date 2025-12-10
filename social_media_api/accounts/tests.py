from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from accounts.models import Accounts
from accounts.serializers import AccountsSerializer


class AccountsAPITestCase(APITestCase):
    """
    Test suite for the Accounts API endpoints.

    This test case covers user registration, authentication, profile management,
    and admin functionality for the social media API accounts system.
    """

    def setUp(self):
        """
        Set up test fixtures before each test method.

        Creates:
        - API client for making requests
        - URL endpoints for various API operations
        - Test user data for registration and authentication
        - A regular user and a superuser in the database
        """
        self.client = APIClient()
        self.serializer = AccountsSerializer

        # API endpoint URLs
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.profile_url = reverse("profile")
        self.logout_url = reverse("logout")
        self.admin_users_url = reverse("admin_users")

        # Test data for a regular user
        self.user_register_data = {
            "username": "testuser",
            "password": "testpassword123",
            "email": "testuser@email.com",
            "first_name": "Test",
            "last_name": "User",
            "bio": "Test bio",
        }

        # Test data for a superuser
        self.create_super_user_register_data = {
            "username": "testuser@1",
            "password": "testpassword123",
            "email": "testuser22@email.com",
            "first_name": "Test",
            "last_name": "User",
            "bio": "Test bio",
        }

        # Create test users in the database
        Accounts.objects.create_user(**self.user_register_data)
        Accounts.objects.create_superuser(**self.create_super_user_register_data)

    def test_duplicate_registration(self):
        """
        Test that duplicate user registration is properly rejected.

        Verifies that:
        - Registration with existing username returns 400 Bad Request
        - Response contains validation errors for username and email
        - Serializer raises ValidationError for duplicate data
        """
        user_data = {
            "username": "testuser",  # Duplicate username
            "password": "testpassword123",
            "email": "testuser@email.com",  # Duplicate email
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword123",
            "password1": "testpassword123",
            "bio": "Test bio",
        }

        # Attempt to register with duplicate credentials
        response = self.client.post(self.register_url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify error messages for duplicate fields
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)

        # Verify serializer validation
        with self.assertRaises(ValidationError):
            self.serializer(data=user_data).is_valid(raise_exception=True)

    def test_login(self):
        """
        Test successful user login with valid credentials.

        Verifies that a user can login with correct username and password,
        and receives a 200 OK response.
        """
        response = self.client.post(
            self.login_url,
            {
                "username": self.user_register_data["username"],
                "password": self.user_register_data["password"],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_confirm_password(self):
        """
        Test successful user registration with matching passwords.

        Verifies that when password and password1 match, the user is
        successfully registered and receives a 201 Created response.
        """
        user_data = {
            "username": "testuser1",
            "password": "testpassword123",
            "email": "testuser1@email.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "testpassword123",  # Matching password confirmation
            "bio": "Test bio",
        }
        response = self.client.post(self.register_url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_password_mismatch(self):
        """
        Test registration failure when passwords don't match.

        Verifies that:
        - Registration fails with 400 Bad Request when password fields mismatch
        - Serializer raises ValidationError for mismatched passwords
        """
        user_data = {
            "username": "testuser2",
            "password": "testpassword123",
            "email": "testuser2@email.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "testpassword1234",  # Mismatched password confirmation
            "bio": "Test bio",
        }
        response = self.client.post(self.register_url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify serializer validation fails
        with self.assertRaises(ValidationError):
            self.serializer(data=user_data).is_valid(raise_exception=True)

    def test_register_weak_password(self):
        """
        Test registration failure with a weak password.

        Verifies that passwords that don't meet strength requirements
        (e.g., too short) are rejected with a 400 Bad Request response.
        """
        user_data = {
            "username": "testuser3",
            "password": "123",  # Weak password - too short
            "email": "testuser3@email.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "123",
            "bio": "Test bio",
        }
        response = self.client.post(self.register_url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify validation error is raised
        with self.assertRaises(ValidationError):
            raise ValidationError("Password is too weak")

    def test_view_profile_without_authentication(self):
        """
        Test that unauthenticated users cannot access profile endpoint.

        Verifies that accessing the profile endpoint without authentication
        returns 401 Unauthorized.
        """
        response = self.client.get(self.profile_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_view_profile_with_authentication(self):
        """
        Test authenticated user can view their profile.

        Verifies that:
        - User can successfully login and receive an auth token
        - Token can be used to access the profile endpoint
        - Profile data matches the authenticated user's information
        """
        # Login to get authentication token
        login_response = self.client.post(
            self.login_url,
            {
                "username": self.user_register_data["username"],
                "password": self.user_register_data["password"],
            },
            format="json",
        )
        token = login_response.data.get("token")

        # Set authentication credentials
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        # Access profile endpoint
        response = self.client.get(self.profile_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["data"]["username"], self.user_register_data["username"]
        )

    def test_view_profile_logout(self):
        """
        Test user logout functionality.

        Verifies that:
        - User can successfully login and receive a token
        - Token can be used to logout
        - Logout endpoint returns success message
        """
        # Login to get authentication token
        login_response = self.client.post(
            self.login_url,
            {
                "username": self.user_register_data["username"],
                "password": self.user_register_data["password"],
            },
            format="json",
        )
        token = login_response.data.get("token")

        # Set authentication credentials
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        # Perform logout
        logout_response = self.client.post(self.logout_url, format="json")
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertIn("detail", logout_response.data)
        self.assertEqual(logout_response.data["detail"], "Successfully logged out.")

    def test_admin_view_users(self):
        """
        Test that admin users can view all users list.

        Verifies that:
        - Superuser can successfully login
        - Superuser can access the admin users endpoint
        - Response contains user data
        """
        # Login as superuser
        login_response = self.client.post(
            self.login_url,
            {
                "username": self.create_super_user_register_data["username"],
                "password": self.create_super_user_register_data["password"],
            },
            format="json",
        )
        token = login_response.data.get("token")

        # Set authentication credentials
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        # Access admin users endpoint
        response = self.client.get(self.admin_users_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)

    def test_not_admin_view_all_users(self):
        """
        Test that non-admin users cannot access admin endpoints.

        Verifies that:
        - Regular user can successfully login
        - Regular user is denied access to admin users endpoint
        - Response returns 403 Forbidden status
        """
        # Login as regular user
        login_response = self.client.post(
            self.login_url,
            {
                "username": self.user_register_data["username"],
                "password": self.user_register_data["password"],
            },
        )
        token = login_response.data.get("token")

        # Set authentication credentials
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        # Attempt to access admin endpoint
        admin_response = self.client.get(self.admin_users_url, format="json")
        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
