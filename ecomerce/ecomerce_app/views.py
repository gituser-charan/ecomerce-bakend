from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import*
from .serializers import*
from .email import*
from django.conf import settings
from django.core.mail import send_mail
import random
from django.http import Http404
from rest_framework import viewsets
class UserRegistrationView(APIView):
    user=CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )
    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        valid = serializers.is_valid(raise_exception = True)
        if valid:
            
            

            serializers.save()
            role = request.data.get('role')
            user = CustomUser.objects.get(role=role)
            if role == 1:
                user.is_superuser=True
                user.save()
            email_otp(serializers.data['email'])
            
            status_code= status.HTTP_201_CREATED
            response={
                'success': True,
                'status': status_code,
                'message' : 'user successfully created',
                'user': serializers.data
           }
            return Response( response, status=status_code)
    
class VerifyOtp(APIView):
    serializer_class = VerifyAccountSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        otp = request.data.get('otp')
        email = request.data.get('email')

        if not email or not otp:
            return Response({'error': 'email and otp is required.'}, status=status.HTTP_400_BAD_REQUEST)
        # Get the user and their associated OTP from the database (assuming you have stored it during registration)
        user = CustomUser.objects.get(email=email) 
        if email != user.email:
            return Response({'error': 'Invalid email.'}, status=status.HTTP_400_BAD_REQUEST)
        # Compare the received OTP with the one in the database
        if otp == user.otp:
            user.is_verified = True
            user.save()
            return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
            
            
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
        
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email']
                    }
                }

            return Response(response, status=status_code)
    
class UserListView(APIView):
    serializer_class = UserListSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        user = CustomUser.objects.all()
        serializer = self.serializer_class(user, many=True)
        response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'users': serializer.data

            }
        return Response(response, status=status.HTTP_200_OK)
    
class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = (AllowAny,)
    def post(self, request):      
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception = True)
        
        if valid:
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            def email_otp(email):
                subject = "Otp for Forgot Passwod"
                otp = random.randint(100000, 999999)
                message = f"your otp is {otp}"
                email_from = settings.EMAIL_HOST
                send_mail(subject, message, email_from, [email] )
                CustomUser_obj = CustomUser.objects.get(email=email)
                CustomUser_obj.otp = otp
                CustomUser_obj.save()
            email_otp(serializer.data['email'])
            
            status_code= status.HTTP_202_ACCEPTED
            response={
                'success': True,
                'status': status_code,
                'message' : 'sent otp succesfully',
                'user': serializer.data
           }
            return Response( response, status=status_code)
        

class ResetPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        otp = request.data.get('otp')
        new = request.data.get('new_password')
        confirm = request.data.get('confirm_new_password')
        
        users = CustomUser.objects.all()
        if not otp:
            return Response({'error': 'OTP is required.'}, status=status.HTTP_400_BAD_REQUEST)
        # Get the user and their associated OTP from the database (assuming you have stored it during registration)
        if new != confirm: 
            return Response({'error': 'New password doesnot match with confirm password.'}, status=status.HTTP_404_NOT_FOUND)
        for user in users:
            user.password = new
            user.save()
        status_code = status.HTTP_200_OK
            

        response = {
            'success': True,
            'statusCode': status_code,
            'message': 'Your password is updated succesfully',
            
        }
        return Response(response, status_code)
    

class UpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UpdateSerializer(user, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoriesViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticated]

class SubCategoriesViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = SubCategories.objects.all()
    serializer_class = SubCategoriesSerializer
    permission_classes = [IsAuthenticated]

class ProductsViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]

class ProductMediaViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = ProductMedia.objects.all()
    serializer_class = ProductMediaSerializer
    permission_classes = [IsAuthenticated]

class ProductTransactionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = ProductTransaction.objects.all()
    serializer_class = ProductTransactionSerializer
    permission_classes = [IsAuthenticated]

class ProductDetailsViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = ProductDetails.objects.all()
    serializer_class = ProductDetailsSerializer
    permission_classes = [IsAuthenticated]




class ProductQuestionsViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = ProductQuestions.objects.all()
    serializer_class = ProductQuestionsSerializer
    permission_classes = [IsAuthenticated]

class ProductReviewsViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = ProductReviews.objects.all()
    serializer_class = ProductReviewsSerializer
    permission_classes = [IsAuthenticated]

class ProductReviewVotingViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = ProductReviewVoting.objects.all()
    serializer_class = ProductReviewVotingSerializer
    permission_classes = [IsAuthenticated]



class CustomerOrdersViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = CustomerOrders.objects.all()
    serializer_class = CustomerOrdersSerializer
    permission_classes = [IsAuthenticated]

class OrderDeliveryStatusViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = OrderDeliveryStatus.objects.all()
    serializer_class = OrderDeliveryStatusSerializer
    permission_classes = [IsAuthenticated]

# Create your views here.

