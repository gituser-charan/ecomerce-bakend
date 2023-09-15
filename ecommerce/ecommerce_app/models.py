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
    is_staff = models.BooleanField(default=False)
    address = models.TextField(max_length=1000, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_by = models.EmailField()
    modified_by = models.EmailField()

    
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

class Brand(models.Model):
    brand_name = models.CharField(max_length=225)
    brand_image = models.ImageField(upload_to='images/')
    
class Products(models.Model):
    subcategories_id=models.ForeignKey(SubCategories,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    variant_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)

class ProductMedia(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    media_type_choice=((1,"Image"),(2,"Video"))
    media_type=models.CharField(max_length=255)
    media_content=models.FileField()
    created_at=models.DateTimeField(auto_now_add=True)
    

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
    image = models.ImageField(upload_to='images/')

class UserProfile(models.Model):

    MALE = 1
    FEMALE = 2
    OTHERS = 3

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERS, 'Others')
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    shipping_address = models.TextField()
    date_of_birth = models.DateField(null=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES)
    mobile = models.BigIntegerField(unique=True, validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(1000000000)
        ])
    display_pic = models.ImageField(upload_to='images/', default='default.png')

class ProductQuestions(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    question=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

class ProductAnswer(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    question_id = models.ForeignKey(ProductQuestions,on_delete=models.CASCADE)
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    answers=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    

class ProductReviews(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    review_image=models.FileField()
    rating=models.SmallIntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],)
    review=models.TextField(default="")
    created_at=models.DateTimeField(auto_now_add=True)
    
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(ProductVariant, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField('ProductVariant', through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.first_name} - {self.total_price}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ])
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Payment for Order {self.order} - {self.user.first_name} - {self.amount}"