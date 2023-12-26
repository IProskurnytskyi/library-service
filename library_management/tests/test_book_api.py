from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from library_management.models import Book
from library_management.serializers import BookSerializer


class UnauthenticatedBookTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            inventory=12,
            daily_fee=23.23
        )

    def test_get_all_books(self) -> None:
        url = reverse("library_management:book-list")
        response = self.client.get(url)

        serializer = BookSerializer(self.book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer.data, response.data)

    def test_get_single_book(self) -> None:
        url = reverse("library_management:book-detail", args=[self.book.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self) -> None:
        url = reverse("library_management:book-list")
        data = {
            "title": "New Book",
            "author": "New Author",
            "inventory": 12,
            "daily_fee": 23.23
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book(self) -> None:
        url = reverse("library_management:book-detail", args=[self.book.id])
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book(self) -> None:
        url = reverse("library_management:book-detail", args=[self.book.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            inventory=12,
            daily_fee=23.23
        )
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="12345",
            first_name="Bob",
            last_name="Ross"
        )
        self.client.force_authenticate(self.user)

    def test_create_book_authorized_forbidden(self) -> None:
        url = reverse("library_management:book-list")
        data = {
            "title": "New Book",
            "author": "New Author",
            "inventory": 12,
            "daily_fee": 23.23
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authorized_forbidden(self) -> None:
        url = reverse("library_management:book-detail", args=[self.book.id])
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authorized_forbidden(self) -> None:
        url = reverse("library_management:book-detail", args=[self.book.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            inventory=12,
            daily_fee=23.23
        )
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="12345",
            first_name="Bob",
            last_name="Ross",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_book_admin(self) -> None:
        url = reverse("library_management:book-list")
        data = {
            "title": "New Book",
            "author": "New Author",
            "inventory": 12,
            "daily_fee": 23.23
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book_admin(self) -> None:
        url = reverse("library_management:book-detail", args=[self.book.id])
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_delete_book_admin(self) -> None:
        url = reverse("library_management:book-detail", args=[self.book.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
