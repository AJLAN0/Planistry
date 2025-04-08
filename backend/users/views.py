from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
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
)
from core.utils import create_response

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
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return create_response(
                data={
                    'token': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                },
                message="Login successful"
            )
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

class UserLogoutView(APIView):
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
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    @swagger_auto_schema(
        operation_summary="Request password reset",
        operation_description="Send a password reset email to the user",
        tags=['Authentication'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email')
            }
        ),
        responses={200: 'Password reset email sent'}
    )
    def post(self, request):
        # Implementation for password reset
        # This would typically involve sending a reset email
        return Response({'detail': 'Password reset email sent'})

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Get user profile",
        operation_description="Retrieve the authenticated user's profile",
        tags=['Profile'],
        responses={200: UserProfileSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_object(self):
        # This ensures we are getting the logged-in user
        return self.request.user

class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="Update user profile",
        operation_description="Update the authenticated user's profile",
        tags=['Profile'],
        request_body=UserProfileSerializer,
        responses={200: UserProfileSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    def get_object(self):
        return self.request.user

class UserPreferencesView(generics.RetrieveAPIView):
    serializer_class = UserPreferencesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Get user preferences",
        operation_description="Retrieve the authenticated user's preferences",
        tags=['Preferences'],
        responses={200: UserPreferencesSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        # Fetch the preferences related to the authenticated user
        return self.request.user.detailed_preferences


class UserPreferencesUpdateView(generics.UpdateAPIView):
    serializer_class = UserPreferencesSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="Update user preferences",
        operation_description="Update the authenticated user's preferences",
        tags=['Preferences'],
        request_body=UserPreferencesSerializer,
        responses={200: UserPreferencesSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    def get_object(self):
        preferences, created = UserPreferences.objects.get_or_create(
            user=self.request.user
        )
        return preferences
