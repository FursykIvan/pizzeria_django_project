from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class PizzaType(models.Model):
    name = models.CharField(max_length=70, unique=True)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    pizza_type = models.ForeignKey(PizzaType, on_delete=models.CASCADE,
                                  related_name="pizzas")
    pizzaioli = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="pizzas")

    def __str__(self):
        return (f"{self.pizza_type}: "
                f"{self.name} (${self.price}) {self.description} "
                f"{self.pizzaioli.name}")
