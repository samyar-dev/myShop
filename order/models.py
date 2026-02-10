from django.db import models
from shop.models import Product

# Create your models here.

class Order(models.Model):
    class Status(models.TextChoices):
        REVIEW = 'review', 'در صف بررسی'
        CONFIRM = 'confirm', 'تایید سفارش'
        DELIVERY = 'delivery', 'تحویل مرسوله'
        PREPARATION = 'preparation', 'اماده سازی سفارش'
        POST = 'post', 'تحویل به پست'
        CANCEL = 'cancel', 'عدم تایید سفارش'

    buyer = models.ForeignKey('account.ShopUser', related_name="orders", on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    address = models.OneToOneField('account.Address', related_name="order_address", on_delete=models.SET_NULL, null=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=250, choices=Status, default=Status.REVIEW)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        
    def __str__(self):
        return f"order ID: {self.id}"

    def get_total_price(self):
        return sum(self.items.price.all())

class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name="order_prods", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField(default=0)
    quantity = models.PositiveBigIntegerField(default=1)
    weight = models.PositiveBigIntegerField(null=True)