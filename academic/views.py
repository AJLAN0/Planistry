from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework_swagger import renderers
from .models import Semester, Course, Assignment
from .serializers import (
    SemesterSerializer,
    CourseSerializer,
    AssignmentSerializer,
)

# Create your views here.

class SemesterListCreateView(generics.ListCreateAPIView):
    """List and create semesters for the authenticated user"""
    serializer_class = SemesterSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Semester.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SemesterDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a semester"""
    serializer_class = SemesterSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Semester.objects.filter(user=self.request.user)

class SemesterNotActiveView(APIView):
    """Mark an assignment as submitted"""
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, pk):
        semester = get_object_or_404(Semester,pk=pk,user=request.user)
        semester.is_active = False
        semester.save()
        return Response({'detail': 'Semester Deactivatied'}, status=status.HTTP_200_OK)
    
class SemesterActiveView(APIView):
    """Mark an assignment as submitted"""
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, pk):
        semester = get_object_or_404(Semester,pk=pk,user=request.user)
        semester.is_active = True
        semester.save()
        return Response({'detail': 'Semester activatied'}, status=status.HTTP_200_OK) 

class CourseListCreateView(generics.ListCreateAPIView):
    """List and create courses for the authenticated user's semesters"""
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Course.objects.filter(semester__user=self.request.user)
    
    def perform_create(self, serializer):
        semester_id = self.request.data.get('semester')
        semester = get_object_or_404(Semester, id=semester_id, user=self.request.user)
        serializer.save(semester=semester)

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a course"""
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Course.objects.filter(semester__user=self.request.user)

class CourseScheduleView(generics.RetrieveUpdateAPIView):
    """Retrieve or update course schedule information"""
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Course.objects.filter(semester__user=self.request.user)

class AssignmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Assignment.objects.filter(course__semester__user=self.request.user)

    def perform_create(self, serializer):
        course_id = self.request.data.get('course')
        course = get_object_or_404(Course, id=course_id, semester__user=self.request.user)
        serializer.save(course=course)

class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an assignment"""
    serializer_class = AssignmentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Assignment.objects.filter(course__semester__user=self.request.user)

class AssignmentSubmitView(APIView):
    """Mark an assignment as submitted"""
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk, course__semester__user=request.user)
        assignment.status = "submitted"
        assignment.submitted_date = timezone.now()
        assignment.save()
        return Response({'detail': 'Assignment marked as submitted'}, status=status.HTTP_200_OK)

class CourseAssignmentListView(generics.ListAPIView):
    """List all assignments for a specific course"""
    serializer_class = AssignmentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        course_pk = self.kwargs['course_pk']
        return Assignment.objects.filter(
            course__pk=course_pk,
            course__semester__user=self.request.user
        )

class CourseAssignmentsView(generics.ListAPIView):
    """List all assignments for a specific course"""
    serializer_class = AssignmentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        course_pk = self.kwargs['course_pk']
        return Assignment.objects.filter(
            course__pk=course_pk,
            course__semester__user=self.request.user
        )

class UpcomingAssignmentsView(generics.ListAPIView):
    """List all upcoming assignments for the authenticated user"""
    serializer_class = AssignmentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Assignment.objects.filter(
            course__semester__user=self.request.user,
            due_date__gte=timezone.now(),
            submitted=False
        ).order_by('due_date')
