from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
 
class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_summary="Obtain JWT Token",
        operation_description="Get JWT access and refresh tokens by providing email and password",
        tags=['Authentication'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email', 'password']
        )
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
                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['refresh']
        )
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# User Registration
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

User = get_user_model()
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return create_response(
                success=False,
                message="Invalid input",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return create_response(
                success=False,
                message="No user found with this email address",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return create_response(
                success=False,
                message="Account is inactive. Please verify your email.",
                status_code=status.HTTP_403_FORBIDDEN
            )

        if not user.check_password(password):
            return create_response(
                success=False,
                message="Incorrect password",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return create_response(
            success=True,
            message="Login successful",
            data={
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data
            }
        )


class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return create_response(message="Successfully logged out", status=status.HTTP_205_RESET_CONTENT)
            except Exception:
                pass
        return create_response(success=False, message="Invalid refresh token", status=status.HTTP_400_BAD_REQUEST)

# Password Reset Request
class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = get_object_or_404(User, email=email)

        cache_key = f'password_reset_{email}'
        if cache.get(cache_key):
            return create_response(success=False, message="Please wait before trying again.", status=status.HTTP_429_TOO_MANY_REQUESTS)

        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        send_mail(
            'Password Reset - Planistry',
            f'Click to reset your password: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )

        cache.set(cache_key, True, 300)
        return create_response(message="Password reset email sent")

# Password Reset Confirm
class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return create_response(success=False, message="Invalid or expired token", status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['password'])
        user.save()
        return create_response(message="Password reset successful")

# User Profile Views
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()

# User Preferences Views
class UserPreferencesView(generics.RetrieveAPIView):
    serializer_class = UserPreferencesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, created = UserPreferences.objects.get_or_create(user=self.request.user)
        return obj

class UserPreferencesUpdateView(generics.UpdateAPIView):
    serializer_class = UserPreferencesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, created = UserPreferences.objects.get_or_create(user=self.request.user)
        return obj

# Test Email View (explicit logic)
class TestEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        send_mail(
            'Test Email',
            'Email configuration test.',
            settings.DEFAULT_FROM_EMAIL,
            ['aj0ly.hd@gmail.com']
        )
        return create_response(message="Test email sent")