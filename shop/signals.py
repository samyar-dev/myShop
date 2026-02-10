from .models import Product
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Product)
def calculate_new_price(sender, instance, **kwargs):
    instance.new_price = instance.price * instance.discount