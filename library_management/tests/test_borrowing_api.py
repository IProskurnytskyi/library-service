from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from library_management.models import Borrowing, Book


class FilteringAndCreatingBorrowTest(TestCase):
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
        self.user_2 = get_user_model().objects.create_user(
            email="user@gmail.com",
            password="12345",
            first_name="Nickola",
            last_name="Tesla",
            is_staff=True
        )
        self.borrowing_1 = Borrowing.objects.create(
            borrow_date="2023-11-11",
            expected_return_date="2023-11-12",
            book=self.book,
            user=self.user
        )
        self.borrowing_2 = Borrowing.objects.create(
            borrow_date="2023-11-12",
            expected_return_date="2023-11-12",
            actual_return_date="2023-11-12",
            book=self.book,
            user=self.user
        )
        self.borrowing_3 = Borrowing.objects.create(
            borrow_date="2023-11-12",
            expected_return_date="2023-11-12",
            actual_return_date="2023-11-12",
            book=self.book,
            user=self.user_2
        )
        self.client.force_authenticate(self.user_2)

    def test_filter_by_user_id(self) -> None:
        url = reverse("library_management:borrowing-list")
        user_id = self.user.id
        response = self.client.get(url, {"user_id": user_id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_active_status_true(self) -> None:
        url = reverse("library_management:borrowing-list")
        response = self.client.get(url, {"is_active": "true"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_active_status_false(self) -> None:
        url = reverse("library_management:borrowing-list")
        response = self.client.get(url, {"is_active": "false"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_borrowing_and_decrease_book_inventory(self) -> None:
        url = reverse("library_management:borrowing-list")
        self.book_2 = Book.objects.create(
            title="Test Book",
            author="Test Author",
            inventory=12,
            daily_fee=23.23
        )
        data = {
            "borrow_date": "2023-11-12",
            "expected_return_date": "2023-11-12",
            "actual_return_date": "2023-11-12",
            "book": self.book_2.id,
        }

        initial_inventory = self.book_2.inventory

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        updated_book = Book.objects.get(id=self.book_2.id)
        self.assertEqual(updated_book.inventory, initial_inventory - 1)
