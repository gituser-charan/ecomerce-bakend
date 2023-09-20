from rest_framework import serializers
from .models import*
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password', 'role')
    
    def create(self, validated_data):
        auth_user = CustomUser.objects.create_user(**validated_data)
        return auth_user

class VerifyAccountSerializer(serializers.Serializer):
    class Meta:
        
        
        email = models.EmailField()
        otp = models.CharField(max_length=6)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    # is_verified = serializers.BooleanField(default=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
        
class ResetPasswordSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        email = serializers.EmailField()
        otp = models.CharField(max_length=6)
        new_password = serializers.CharField(max_length=20, write_only=True)
        confirm_new_password = serializers.CharField(max_length=20, write_only=True)

        def create(self, validated_data):
            auth_user = CustomUser.objects.create_user(**validated_data)
            return auth_user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"

class SubCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategories
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"

class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = "__all__"

class ProductTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTransaction
        fields = "__all__"

class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetails
        fields = "__all__"

class ProductQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductQuestions
        fields = "__all__"

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAnswer
        fields = "__all__"

class ProductReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReviews
        fields = "__all__"

class VarientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"