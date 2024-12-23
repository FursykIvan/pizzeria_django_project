from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.services.token_service import account_activation_token
from django.contrib.auth import get_user_model
from accounts.models import Pizzaiolo
from kitchen.models import Pizza, PizzaType


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

User = get_user_model()

class KitchenViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password123")
        cls.pizza_type = PizzaType.objects.create(name="Vegetarian")
        cls.pizza = Pizza.objects.create(
            name="Margherita",
            description="Classic pizza with tomatoes and mozzarella",
            price=10.00,
            pizza_type=cls.pizza_type,
        )
        cls.pizza.pizzaioli.set([cls.user])

    def setUp(self):
        self.client.login(username="testuser", password="password123")

    def test_home_page_view(self):
        response = self.client.get(reverse("kitchen:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_pizza_detail_view(self):
        response = self.client.get(reverse("kitchen:pizza-detail", kwargs={"pk": self.pizza.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/pizza_detail.html")
        self.assertContains(response, "Margherita")

    def test_pizza_create_view(self):
        response = self.client.post(
            reverse("kitchen:pizza-create"),
            data={
                "name": "Pepperoni",
                "description": "Spicy pizza with pepperoni",
                "price": 12.50,
                "pizza_type": self.pizza_type.id,
                "pizzaioli": [self.user.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Pizza.objects.filter(name="Pepperoni").exists())

    def test_pizza_update_view(self):
        response = self.client.post(
            reverse("kitchen:pizza-update", kwargs={"pk": self.pizza.pk}),
            data={
                "name": "Margherita Updated",
                "description": "Updated description",
                "price": 11.00,
                "pizza_type": self.pizza_type.id,
                "pizzaioli": [self.user.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.pizza.refresh_from_db()
        self.assertEqual(self.pizza.name, "Margherita Updated")

    def test_pizza_delete_view(self):
        response = self.client.post(reverse("kitchen:pizza-delete", kwargs={"pk": self.pizza.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Pizza.objects.filter(pk=self.pizza.pk).exists())

    def test_pizza_type_create_view(self):
        response = self.client.post(
            reverse("kitchen:pizza-type-create"), data={"name": "Meat Lover"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PizzaType.objects.filter(name="Meat Lover").exists())

    def test_pizza_type_update_view(self):
        response = self.client.post(
            reverse("kitchen:pizza-type-update", kwargs={"pk": self.pizza_type.pk}),
            data={"name": "Vegetarian Updated"},
        )
        self.assertEqual(response.status_code, 302)
        self.pizza_type.refresh_from_db()
        self.assertEqual(self.pizza_type.name, "Vegetarian Updated")

    def test_pizza_type_delete_view(self):
        response = self.client.post(reverse("kitchen:pizza-type-delete", kwargs={"pk": self.pizza_type.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(PizzaType.objects.filter(pk=self.pizza_type.pk).exists())
