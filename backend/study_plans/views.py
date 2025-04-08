from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import StudyPlan, StudySession, Goal
from .serializers import (
    StudyPlanSerializer,
    StudySessionSerializer,
    GoalSerializer,
)
from django.db import models

# Create your views here.

class StudyPlanListCreateView(generics.ListCreateAPIView):
    serializer_class = StudyPlanSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="List and create study plans",
        operation_description="Get a list of all study plans or create a new one",
        tags=['Study Plans'],
        responses={200: StudyPlanSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create study plan",
        operation_description="Create a new study plan",
        tags=['Study Plans'],
        request_body=StudyPlanSerializer,
        responses={201: StudyPlanSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        return StudyPlan.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StudyPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudyPlanSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="Get study plan details",
        operation_description="Get details of a specific study plan",
        tags=['Study Plans'],
        responses={200: StudyPlanSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update study plan",
        operation_description="Update a specific study plan",
        tags=['Study Plans'],
        request_body=StudyPlanSerializer,
        responses={200: StudyPlanSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete study plan",
        operation_description="Delete a specific study plan",
        tags=['Study Plans'],
        responses={204: 'No content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    def get_queryset(self):
        return StudyPlan.objects.filter(user=self.request.user)

class StudySessionListCreateView(generics.ListCreateAPIView):
    serializer_class = StudySessionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="List and create study sessions",
        operation_description="Get a list of all study sessions or create a new one",
        tags=['Study Sessions'],
        responses={200: StudySessionSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create study session",
        operation_description="Create a new study session",
        tags=['Study Sessions'],
        request_body=StudySessionSerializer,
        responses={201: StudySessionSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        return StudySession.objects.filter(study_plan__user=self.request.user)
    
    def perform_create(self, serializer):
        study_plan = get_object_or_404(StudyPlan, pk=self.kwargs['plan_pk'], user=self.request.user)
        serializer.save(study_plan=study_plan)

class StudySessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudySessionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="Get study session details",
        operation_description="Get details of a specific study session",
        tags=['Study Sessions'],
        responses={200: StudySessionSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update study session",
        operation_description="Update a specific study session",
        tags=['Study Sessions'],
        request_body=StudySessionSerializer,
        responses={200: StudySessionSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete study session",
        operation_description="Delete a specific study session",
        tags=['Study Sessions'],
        responses={204: 'No content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    def get_queryset(self):
        return StudySession.objects.filter(study_plan__user=self.request.user)

class GoalListCreateView(generics.ListCreateAPIView):
    serializer_class = GoalSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="List and create goals",
        operation_description="Get a list of all goals or create a new one",
        tags=['Goals'],
        responses={200: GoalSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create goal",
        operation_description="Create a new goal",
        tags=['Goals'],
        request_body=GoalSerializer,
        responses={201: GoalSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        return Goal.objects.filter(study_plan__user=self.request.user)
    
    def perform_create(self, serializer):
        study_plan = get_object_or_404(StudyPlan, pk=self.kwargs['plan_pk'], user=self.request.user)
        serializer.save(study_plan=study_plan)

class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="Get goal details",
        operation_description="Get details of a specific goal",
        tags=['Goals'],
        responses={200: GoalSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update goal",
        operation_description="Update a specific goal",
        tags=['Goals'],
        request_body=GoalSerializer,
        responses={200: GoalSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete goal",
        operation_description="Delete a specific goal",
        tags=['Goals'],
        responses={204: 'No content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    def get_queryset(self):
        return Goal.objects.filter(study_plan__user=self.request.user)

class StudyPlanProgressView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="Get study plan progress",
        operation_description="Get progress statistics for a specific study plan",
        tags=['Study Plans'],
        responses={
            200: openapi.Response(
                description="Study plan progress statistics",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_goals': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'completed_goals': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'completion_rate': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'total_sessions': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_duration': openapi.Schema(type=openapi.TYPE_NUMBER)
                    }
                )
            )
        }
    )
    def get(self, request, pk):
        study_plan = get_object_or_404(StudyPlan, pk=pk, user=request.user)
        total_goals = study_plan.goals.count()
        completed_goals = study_plan.goals.filter(status='completed').count()
        total_sessions = study_plan.study_sessions.count()
        total_duration = study_plan.study_sessions.aggregate(total_duration=models.Sum('duration'))['total_duration'] or 0
        
        return Response({
            'total_goals': total_goals,
            'completed_goals': completed_goals,
            'completion_rate': (completed_goals / total_goals * 100) if total_goals > 0 else 0,
            'total_sessions': total_sessions,
            'total_duration': total_duration,
        })
