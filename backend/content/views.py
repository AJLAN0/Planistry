from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import CourseFile, StudyMaterial, Note
from .serializers import (
    CourseFileSerializer,
    StudyMaterialSerializer,
    NoteSerializer,
)

# Create your views here.

class CourseFileListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseFileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="List and create course files",
        operation_description="Get a list of all course files or create a new one",
        tags=['Course Files'],
        responses={200: CourseFileSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create course file",
        operation_description="Create a new course file",
        tags=['Course Files'],
        request_body=CourseFileSerializer,
        responses={201: CourseFileSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        return CourseFile.objects.filter(course__semester__user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save()

class CourseFileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseFileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="Get course file details",
        operation_description="Get details of a specific course file",
        tags=['Course Files'],
        responses={200: CourseFileSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update course file",
        operation_description="Update a specific course file",
        tags=['Course Files'],
        request_body=CourseFileSerializer,
        responses={200: CourseFileSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete course file",
        operation_description="Delete a specific course file",
        tags=['Course Files'],
        responses={204: 'No content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    def get_queryset(self):
        return CourseFile.objects.filter(course__semester__user=self.request.user)

class StudyMaterialListCreateView(generics.ListCreateAPIView):
    serializer_class = StudyMaterialSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="List and create study materials",
        operation_description="Get a list of all study materials or create a new one",
        tags=['Study Materials'],
        responses={200: StudyMaterialSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create study material",
        operation_description="Create a new study material",
        tags=['Study Materials'],
        request_body=StudyMaterialSerializer,
        responses={201: StudyMaterialSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        return StudyMaterial.objects.filter(course__semester__user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save()

class StudyMaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudyMaterialSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="Get study material details",
        operation_description="Get details of a specific study material",
        tags=['Study Materials'],
        responses={200: StudyMaterialSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update study material",
        operation_description="Update a specific study material",
        tags=['Study Materials'],
        request_body=StudyMaterialSerializer,
        responses={200: StudyMaterialSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete study material",
        operation_description="Delete a specific study material",
        tags=['Study Materials'],
        responses={204: 'No content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    def get_queryset(self):
        return StudyMaterial.objects.filter(course__semester__user=self.request.user)

class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="List and create notes",
        operation_description="Get a list of all notes or create a new one",
        tags=['Notes'],
        responses={200: NoteSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create note",
        operation_description="Create a new note",
        tags=['Notes'],
        request_body=NoteSerializer,
        responses={201: NoteSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        return Note.objects.filter(course__semester__user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save()

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="Get note details",
        operation_description="Get details of a specific note",
        tags=['Notes'],
        responses={200: NoteSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update note",
        operation_description="Update a specific note",
        tags=['Notes'],
        request_body=NoteSerializer,
        responses={200: NoteSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete note",
        operation_description="Delete a specific note",
        tags=['Notes'],
        responses={204: 'No content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    def get_queryset(self):
        return Note.objects.filter(course__semester__user=self.request.user)

class CourseContentListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="List course content",
        operation_description="Get a list of content for a specific course",
        tags=['Course Content'],
        manual_parameters=[
            openapi.Parameter(
                'type',
                openapi.IN_QUERY,
                description="Content type filter (file, material, note)",
                type=openapi.TYPE_STRING,
                enum=['file', 'material', 'note']
            )
        ],
        responses={
            200: openapi.Response(
                description="Course content list",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        oneOf=[
                            CourseFileSerializer,
                            StudyMaterialSerializer,
                            NoteSerializer
                        ]
                    )
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        course_pk = self.kwargs['course_pk']
        content_type = self.request.query_params.get('type', None)
        
        if content_type == 'file':
            return CourseFile.objects.filter(course_id=course_pk, course__semester__user=self.request.user)
        elif content_type == 'material':
            return StudyMaterial.objects.filter(course_id=course_pk, course__semester__user=self.request.user)
        elif content_type == 'note':
            return Note.objects.filter(course_id=course_pk, course__semester__user=self.request.user)
        
        return []
    
    def get_serializer_class(self):
        content_type = self.request.query_params.get('type', None)
        
        if content_type == 'file':
            return CourseFileSerializer
        elif content_type == 'material':
            return StudyMaterialSerializer
        elif content_type == 'note':
            return NoteSerializer
        
        return CourseFileSerializer  # default serializer

class CourseFileDownloadView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_summary="Download course file",
        operation_description="Download a specific course file",
        tags=['Course Files'],
        responses={
            200: openapi.Response(
                description="File download response",
                schema=openapi.Schema(type=openapi.TYPE_FILE)
            )
        }
    )
    def get(self, request, pk):
        course_file = get_object_or_404(CourseFile, pk=pk, course__semester__user=request.user)
        return FileResponse(course_file.file, as_attachment=True, filename=course_file.file.name)
