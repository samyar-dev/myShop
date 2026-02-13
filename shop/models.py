from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator
# from account.models import ShopUser
import os
from django.shortcuts import reverse
# from decimal import Decimal
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    
    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('shop:products_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    description = models.CharField(max_length=2500)
    inventory = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    discount = models.FloatField(default=0)
    weight = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField('account.ShopUser', related_name='likes', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def new_price(self):
        discount_price = self.price - (self.price * self.discount)
        return discount_price
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    
    def get_absolute_url(self):
        return reverse('shop:product', kwargs={'id': self.id, 'slug': self.slug})


class ProductFeatures(models.Model):
    product = models.ForeignKey(Product, related_name="features", on_delete=models.CASCADE, null=True, blank=True)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.key} : {self.value}"


class Image(models.Model):
    prudoct = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image_file = models.ImageField(upload_to="images/%Y/")
    title = models.CharField(max_length=250, null=True, blank=True)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.title if self.title else os.path.basename(self.image_file.name)
