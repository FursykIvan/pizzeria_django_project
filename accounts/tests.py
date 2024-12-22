from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.services.token_service import account_activation_token
from django.contrib.auth import get_user_model
from accounts.models import Pizzaiolo


class PizzaioloModelTest(TestCase):
    def test_pizzaiolo_creation(self):
        pizzaiolo = Pizzaiolo.objects.create_user(
            username="testuser", email="test@example.com", password="password123", year_of_experience=5
        )
        self.assertEqual(pizzaiolo.username, "testuser")
        self.assertEqual(pizzaiolo.email, "test@example.com")
        self.assertEqual(pizzaiolo.year_of_experience, 5)

    def test_pizzaiolo_string_representation(self):
        pizzaiolo = Pizzaiolo.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.assertEqual(str(pizzaiolo), "testuser")


class AccountViewsTest(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)

    def test_activate_view(self):
        pizzaiolo = Pizzaiolo.objects.create_user(
            username="testuser", email="test@example.com", password="password123", is_active=False
        )
        uid = urlsafe_base64_encode(force_bytes(pizzaiolo.pk))
        token = account_activation_token.make_token(pizzaiolo)

        activation_url = reverse("accounts:activate", kwargs={"uid": uid, "token": token})
        response = self.client.get(activation_url)

        pizzaiolo.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(pizzaiolo.is_active)


class PizzaioloDetailViewTest(TestCase):
    def test_pizzaiolo_detail_view(self):
        user = get_user_model().objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

        response = self.client.get(reverse("accounts:profile", kwargs={"pk": user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
