from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from kitchen.models import Pizza, PizzaType

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
