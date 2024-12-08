from django.db import models
from django.contrib.auth.models import AbstractUser


class Pizzaiolo(AbstractUser):
    year_of_experience = models.PositiveSmallIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ("username",)
        verbose_name = "Pizzaiolo"
        verbose_name_plural = "Pizzaioli"


    def __str__(self):
        return self.username
