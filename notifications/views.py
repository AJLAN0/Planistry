from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="List notifications",
        operation_description="Get a list of all notifications for the authenticated user",
        tags=['Notifications'],
        responses={200: NotificationSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="Get notification details",
        operation_description="Get details of a specific notification",
        tags=['Notifications'],
        responses={200: NotificationSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update notification",
        operation_description="Update a specific notification",
        tags=['Notifications'],
        request_body=NotificationSerializer,
        responses={200: NotificationSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete notification",
        operation_description="Delete a specific notification",
        tags=['Notifications'],
        responses={204: 'No content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class NotificationMarkReadView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="Mark notification as read",
        operation_description="Mark a specific notification as read",
        tags=['Notifications'],
        responses={
            200: openapi.Response(
                description="Success response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({'detail': 'Notification marked as read'})

class NotificationMarkAllReadView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="Mark all notifications as read",
        operation_description="Mark all notifications as read for the authenticated user",
        tags=['Notifications'],
        responses={
            200: openapi.Response(
                description="Success response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def post(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'detail': 'All notifications marked as read'})

class NotificationClearView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="Clear all notifications",
        operation_description="Delete all notifications for the authenticated user",
        tags=['Notifications'],
        responses={
            200: openapi.Response(
                description="Success response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def post(self, request):
        Notification.objects.filter(user=request.user).delete()
        return Response({'detail': 'All notifications cleared'})
