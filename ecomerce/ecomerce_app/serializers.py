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
        
        otp = models.CharField(max_length=6)
        new_password = serializers.CharField(max_length=20, write_only=True)
        confirm_new_password = serializers.CharField(max_length=20, write_only=True)

        def create(self, validated_data):
            auth_user = CustomUser.objects.create_user(**validated_data)
            return auth_user

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'date_of_birth', 'gender', 'mobile', 'display_pic', 'address')

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"

class SubCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategories
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

class ProductReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReviews
        fields = "__all__"

class ProductReviewVotingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReviewVoting
        fields = "__all__"

class CustomerOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOrders
        fields = "__all__"

class OrderDeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDeliveryStatus
        fields = "__all__"
