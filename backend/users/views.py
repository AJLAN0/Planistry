from django.shortcuts import render
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User, UserPreferences
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserPreferencesSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from core.utils import create_response
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetConfirmView as DjangoPasswordResetConfirmView
from django.core.cache import cache

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Create a new user account with email and password",
        tags=['Authentication'],
        responses={201: UserSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    @swagger_auto_schema(
        operation_summary="Login user",
        operation_description="Login with email and password to receive JWT tokens",
        tags=['Authentication'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Login successful",
                        "data": {
                            "token": "your_jwt_token_here",
                            "user": {
                                "id": 1,
                                "email": "user@example.com",
                                "username": "username",
                                "first_name": "John",
                                "last_name": "Doe",
                                "profile": {
                                    "avatar": "url_to_avatar",
                                    "bio": "User bio"
                                }
                            }
                        }
                    }
                }
            )
        }
    )
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if not serializer.is_valid():
                return create_response(
                    success=False,
                    message="Invalid credentials",
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
            except User.DoesNotExist:
                return create_response(
                    success=False,
                    message="No active account found with the given credentials",
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
            if not user.is_active:
                return create_response(
                    success=False,
                    message="Account is not active. Please check your email for activation link.",
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if user.check_password(serializer.validated_data['password']):
                refresh = RefreshToken.for_user(user)
                return create_response(
                    data={
                        'token': str(refresh),
                        'access': str(refresh.access_token),
                        'user': UserSerializer(user).data
                    },
                    message="Login successful"
                )
            else:
                return create_response(
                    success=False,
                    message="Invalid password",
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception:
            return create_response(
                success=False,
                message="Invalid credentials",
                status=status.HTTP_401_UNAUTHORIZED
            )

class UserLogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JWTAuthentication]
    
    @swagger_auto_schema(
        operation_summary="Logout user",
        operation_description="Blacklist the refresh token to logout",
        tags=['Authentication'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token')
            }
        ),
        responses={
            205: 'Successfully logged out',
            400: 'Bad request'
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return create_response(
                    success=False,
                    message="Refresh token is required",
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return create_response(
                    message="Successfully logged out",
                    status=status.HTTP_205_RESET_CONTENT
                )
            except Exception:
                return create_response(
                    success=False,
                    message="Invalid refresh token",
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception:
            return create_response(
                success=False,
                message="Invalid request",
                status=status.HTTP_400_BAD_REQUEST
            )

class PasswordResetView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    @swagger_auto_schema(
        operation_summary="Request password reset",
        operation_description="Send a password reset email to the user",
        tags=['Authentication'],
        request_body=PasswordResetRequestSerializer,
        responses={
            200: openapi.Response(
                description="Password reset email sent successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Password reset email has been sent"
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid email",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "No user found with this email address"
                    }
                }
            )
        }
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        # Rate limiting
        cache_key = f'password_reset_{email}'
        if cache.get(cache_key):
            return Response(
                {'error': 'Please wait before requesting another password reset'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        try:
            user = User.objects.get(email=email)
            
            # Generate a unique token
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create reset link
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            
            # Send email
            subject = 'Password Reset Request - Planistry'
            message = f"""
            Hello {user.get_full_name() or user.email},
            
            You have requested to reset your password. Please click the link below to reset your password:
            
            {reset_link}
            
            If you did not request this password reset, please ignore this email.
            
            This link will expire in 1 hour.
            
            Best regards,
            Planistry Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            # Set rate limit (1 request per 5 minutes)
            cache.set(cache_key, True, 300)
            
            return create_response(
                message="Password reset email has been sent",
                success=True
            )
            
        except User.DoesNotExist:
            return Response(
                {'error': 'No user found with this email address'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PasswordResetConfirmView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    @swagger_auto_schema(
        operation_summary="Confirm password reset",
        operation_description="Set a new password for the user",
        tags=['Authentication'],
        request_body=PasswordResetConfirmSerializer,
        responses={
            200: openapi.Response(
                description="Password reset successful",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Password has been reset successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid request",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Invalid or expired token"
                    }
                }
            )
        }
    )
    def post(self, request, uidb64, token):
        try:
            # Decode the user ID
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return create_response(
                    success=False,
                    message="Invalid reset link",
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify the token
            if not PasswordResetTokenGenerator().check_token(user, token):
                return create_response(
                    success=False,
                    message="Invalid or expired token",
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate the new password
            serializer = PasswordResetConfirmSerializer(data=request.data)
            if not serializer.is_valid():
                return create_response(
                    success=False,
                    message=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set the new password
            new_password = serializer.validated_data['password']
            user.set_password(new_password)
            user.save()
            
            # Verify the password was set correctly
            if not user.check_password(new_password):
                return create_response(
                    success=False,
                    message="Failed to set new password",
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            return create_response(
                message="Password has been reset successfully",
                success=True
            )
            
        except Exception as e:
            return create_response(
                success=False,
                message="Invalid request",
                status=status.HTTP_400_BAD_REQUEST
            )

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return create_response(data=serializer.data)
    
    def get_object(self):
        return self.request.user

class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return create_response(data=serializer.data,message= "Profile updated successfully")
    
    def get_object(self):
        return self.request.user

class UserPreferencesView(generics.RetrieveAPIView):
    serializer_class = UserPreferencesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return create_response(data=serializer.data)

    def get_object(self):
        preferences, created = UserPreferences.objects.get_or_create(user=self.request.user)
        return preferences

class UserPreferencesUpdateView(generics.UpdateAPIView):
    serializer_class = UserPreferencesSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return create_response(data=serializer.data)
    
    def get_object(self):
        preferences, created = UserPreferences.objects.get_or_create(user=self.request.user)
        return preferences

# JWT Token Views with Swagger Documentation
class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_summary="Obtain JWT Token",
        operation_description="Get JWT access and refresh tokens by providing email and password",
        tags=['Authentication'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            },
            required=['email', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Token obtained successfully",
                examples={
                    "application/json": {
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_summary="Refresh JWT Token",
        operation_description="Get a new access token using a refresh token",
        tags=['Authentication'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token'),
            },
            required=['refresh']
        ),
        responses={
            200: openapi.Response(
                description="Token refreshed successfully",
                examples={
                    "application/json": {
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TestEmailView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    @swagger_auto_schema(
        operation_summary="Test email configuration",
        operation_description="Send a test email to verify email configuration",
        tags=['Testing'],
        responses={
            200: openapi.Response(
                description="Test email sent successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Test email has been sent"
                    }
                }
            )
        }
    )
    def get(self, request):
        try:
            from django.core.mail import send_mail
            send_mail(
                'Test Email from Planistry',
                'This is a test email from Planistry. If you receive this, the email configuration is working correctly.',
                settings.DEFAULT_FROM_EMAIL,
                ['aj0ly.hd@gmail.com'],
                fail_silently=False,
            )
            
            return create_response(
                message="Test email has been sent",
                success=True
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
