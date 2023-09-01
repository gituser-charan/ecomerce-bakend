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

class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )
    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        valid = serializers.is_valid(raise_exception = True)
        if valid:
            email_otp(serializers.data['email'])
            serializers.save()
            status_code= status.HTTP_201_CREATED
            response={
                'success': True,
                'status': status_code,
                'message' : 'user successfully created',
                'user': serializers.data
           }
        return Response( response, status=status_code)
    
class VerifyOtp(APIView):
    user = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    def post(self, request):
        otp = request.data.get('otp')
        email = request.data.get('email')

        if not email:
            return Response({'error': 'email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not otp:
            return Response({'error': 'OTP is required.'}, status=status.HTTP_400_BAD_REQUEST)
        # Get the user and their associated OTP from the database (assuming you have stored it during registration)
        user = request.user # Assuming the user is authenticated
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

    def post(self, request):
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
        serializers = self.serializer_class(data=request.data)
        valid = serializers.is_valid(raise_exception = True)
        if valid:
            def email_otp(email):
                subject = "Otp for Forgot Passwod"
                otp = random.randint(100000, 999999)
                message = f"your otp is {otp}"
                email_from = settings.EMAIL_HOST
                send_mail(subject, message, email_from, [email] )
                CustomUser_obj = CustomUser.objects.get(email=email)
                CustomUser_obj.otp = otp
                CustomUser_obj.save()
            email_otp(serializers.data['email'])
            
            status_code= status.HTTP_202_ACCEPTED
            response={
                'success': True,
                'status': status_code,
                'message' : 'sent otp succesfully',
                'user': serializers.data
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
# Create your views here.
