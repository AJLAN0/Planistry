from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import CourseFile, StudyMaterial, Note
from .serializers import CourseFileSerializer, StudyMaterialSerializer, NoteSerializer

class CourseFileListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        #return CourseFile.objects.filter(course__semester__user=self.request.user)
        return CourseFile.objects.all()

class CourseFileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CourseFile.objects.filter(course__semester__user=self.request.user)

class CourseFileDownloadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        course_file = get_object_or_404(CourseFile, pk=pk, course__semester__user=request.user)
        response = HttpResponse(course_file.file, content_type=f'application/{course_file.file_type}')
        response['Content-Disposition'] = f'attachment; filename="{course_file.filename}"'
        return response

class StudyMaterialListCreateView(generics.ListCreateAPIView):
    serializer_class = StudyMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudyMaterial.objects.filter(course__semester__user=self.request.user)

class StudyMaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudyMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudyMaterial.objects.filter(course__semester__user=self.request.user)

class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(course__semester__user=self.request.user)

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(course__semester__user=self.request.user)

class CourseContentListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_pk = self.kwargs['course_pk']
        content_type = self.request.query_params.get('type')

        if content_type == 'file':
            return CourseFile.objects.filter(course_id=course_pk, course__semester__user=self.request.user)
        elif content_type == 'material':
            return StudyMaterial.objects.filter(course_id=course_pk, course__semester__user=self.request.user)
        elif content_type == 'note':
            return Note.objects.filter(course_id=course_pk, course__semester__user=self.request.user)
        return CourseFile.objects.none()

    def get_serializer_class(self):
        content_type = self.request.query_params.get('type')
        if content_type == 'material':
            return StudyMaterialSerializer
        elif content_type == 'note':
            return NoteSerializer
        return CourseFileSerializer
