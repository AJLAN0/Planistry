from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import StudyPlan, StudySession, Goal, StudyTask
from .serializers import (
    StudyPlanSerializer,
    StudySessionSerializer,
    GoalSerializer,
    StudyTaskSerializer,
)
from django.db import models
from django.utils import timezone

# Create your views here.

class StudyPlanListCreateView(generics.ListCreateAPIView):
    serializer_class = StudyPlanSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        return StudyPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StudyPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudyPlanSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return StudyPlan.objects.filter(user=self.request.user)

class StudySessionListCreateView(generics.ListCreateAPIView):
    serializer_class = StudySessionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        return StudySession.objects.filter(study_plan__user=self.request.user)

    def perform_create(self, serializer):
        study_plan = get_object_or_404(StudyPlan, pk=self.kwargs['plan_pk'], user=self.request.user)
        session = serializer.save(study_plan=study_plan)

        # Automatically complete tasks matching the session topic
        matching_tasks = StudyTask.objects.filter(
            study_plan=study_plan, title__iexact=session.topic, status='not_started'
        )
        for task in matching_tasks:
            task.status = 'completed'
            task.completed_at = session.end_time
            task.completed_by = self.request.user
            task.save()

class StudySessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudySessionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return StudySession.objects.filter(study_plan__user=self.request.user)

class GoalListCreateView(generics.ListCreateAPIView):
    serializer_class = GoalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Goal.objects.filter(study_plan__user=self.request.user)

class StudyPlanProgressView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        study_plan = get_object_or_404(StudyPlan, pk=pk, user=request.user)
        total_goals = study_plan.goals.count()
        completed_goals = study_plan.goals.filter(status='completed').count()
        total_sessions = study_plan.study_sessions.count()
        total_duration = study_plan.study_sessions.aggregate(total_duration=models.Sum('duration'))['total_duration'] or 0
        total_tasks = study_plan.tasks.count()
        completed_tasks = study_plan.tasks.filter(status='completed').count()

        return Response({
            'total_goals': total_goals,
            'completed_goals': completed_goals,
            'completion_rate': (completed_goals / total_goals * 100) if total_goals > 0 else 0,
            'total_sessions': total_sessions,
            'total_duration': total_duration,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'task_completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        })

class MarkTaskCompleteView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, task_id):
        task = get_object_or_404(StudyTask, id=task_id, study_plan__user=request.user)
        task.status = 'completed'
        task.completed_by = request.user
        task.completed_at = timezone.now()
        task.save()
        return Response({'status': 'success', 'message': 'Task marked as completed.'})


class StudyTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = StudyTaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return StudyTask.objects.filter(study_plan__user=self.request.user)

    def perform_create(self, serializer):
        study_plan = get_object_or_404(StudyPlan, pk=self.kwargs['plan_pk'], user=self.request.user)
        serializer.save(study_plan=study_plan, completed_by=None, completed_at=None)


class StudyTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudyTaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return StudyTask.objects.filter(study_plan__user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_at=timezone.now())