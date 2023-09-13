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
    is_staff = models.BooleanField(default=False)
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
  
class Categories(models.Model):
    title=models.CharField(max_length=255)
    thumbnail=models.FileField()
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

    def __str__(self):
        return self.title

class SubCategories(models.Model):
    category_id=models.ForeignKey(Categories,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    thumbnail=models.FileField(upload_to='images/')
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)
    
class Products(models.Model):
    subcategories_id=models.ForeignKey(SubCategories,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=255)
    brand=models.CharField(max_length=255)
    product_max_price=models.CharField(max_length=255)
    product_discount_price=models.CharField(max_length=255)
    product_description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    in_stock_total=models.IntegerField(default=1)
    is_active=models.IntegerField(default=1)

class ProductMedia(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    media_type_choice=((1,"Image"),(2,"Video"))
    media_type=models.CharField(max_length=255)
    media_content=models.FileField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)  

class ProductTransaction(models.Model):
    transaction_type_choices=((1,"BUY"),(2,"SELL"))
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    transaction_product_count=models.IntegerField(default=1)
    transaction_type=models.CharField(choices=transaction_type_choices,max_length=255)
    transaction_description=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)


class ProductDetails(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    title_details=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)


class ProductQuestions(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    question=models.TextField()
    answer=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductReviews(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    review_image=models.FileField()
    rating=models.CharField(default="5",max_length=255)
    review=models.TextField(default="")
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductReviewVoting(models.Model):
    product_review_id=models.ForeignKey(ProductReviews,on_delete=models.CASCADE)
    user_id_voting=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)


class CustomerOrders(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.DO_NOTHING)
    purchase_price=models.CharField(max_length=255)
    coupon_code=models.CharField(max_length=255)
    discount_amt=models.CharField(max_length=255)
    product_status=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

class OrderDeliveryStatus(models.Model):
    order_id=models.ForeignKey(CustomerOrders,on_delete=models.CASCADE)
    status=models.CharField(max_length=255)
    status_message=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)