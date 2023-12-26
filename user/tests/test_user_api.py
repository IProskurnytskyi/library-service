from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class CreateUserTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user(self) -> None:
        url = reverse("user:create")
        data = {
            "email": "test@gmail.com",
            "password": "12345",
            "first_name": "Bob",
            "last_name": "Ross"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ManageUserTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="12345",
            first_name="Bob",
            last_name="Ross"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_user(self) -> None:
        url = reverse("user:manage")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_update_user(self) -> None:
        url = reverse("user:manage")
        data = {"email": "update@gmail.com"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "update@gmail.com")
