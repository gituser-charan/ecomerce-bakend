from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import *
# from ecomerce.settings import DATE_TIME_FORMATS
# from ecomerce import settings
from django.utils import timezone
import uuid
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import CustomUserManager
class CustomUser(AbstractBaseUser, PermissionsMixin):
        # These fields tie to the roles!
    ADMIN = 1
    DELIVERY = 2
    EMPLOYEE = 3
    CUSTOMER = 4

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (DELIVERY, 'Delivery'),
        (CUSTOMER, 'Customer'),
        (EMPLOYEE, 'Employee')
    )

    MALE = 1
    FEMALE = 2
    OTHERS = 3

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERS, 'Others')
    )
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, default=000000)
    role = models.PositiveIntegerField(choices=ROLE_CHOICES)
    date_of_birth = models.DateField(null=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True)
    mobile = models.BigIntegerField(unique=True, validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(1000000000)
        ], null=True)
    display_pic = models.ImageField(upload_to='images/', default='default.png')
    address = models.TextField(max_length=1000, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
  

# class Product(models.Model):
#     product_name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     inventory = models.PositiveIntegerField()
#     product_image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    
#     def __str__(self):
#         return self.product_name

# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     items = models.ManyToManyField(Product, through='CartItem')

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     def get_order_price(self):
#         return self.quantity * self.product.price
    
# class Order(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product, through='OrderItem')
#     # status = models.CharField(choices=OrderStatus.choices, max_length=20)
#     created_at = models.DateTimeField(auto_now_add=True)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()

#     def get_order_price(self):
#         return self.quantity * self.product.price

# Create your models here.
