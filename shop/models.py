from statistics import mode
from unittest.util import _MAX_LENGTH

from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField("Status", default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title

    # def total_product(self):
    #     return self.products.count()


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    price = models.FloatField(help_text="USD")
    is_active = models.BooleanField("Status", default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name
