from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from order.models import Order

# Create your models here.

class ShopUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("phone is requared")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, phone, password=None, **extra_fields):
        is_staff_ = extra_fields.setdefault('is_staff', True)
        is_superuser_ = extra_fields.setdefault('is_superuser', True)

        if not is_staff_ & is_superuser_:
            raise ValueError("can not create superuser")
        
        return self.create_user(phone, password=None, **extra_fields)


class ShopUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.OneToOneField('Address', related_name="user_address", on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_join = models.DateTimeField(default=timezone.now)

    objects = ShopUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS: list = [] 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def has_perm_to_see(self, page_id):
        yours_page_id = Order.objects.get(id=page_id)
        return yours_page_id


class Address(models.Model):
    postal_code = models.CharField(max_length=10)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.province} {self.city}"