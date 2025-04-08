from rest_framework import serializers
from .models import CourseFile, StudyMaterial, Note

class CourseFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFile
        fields = ['id', 'title', 'file', 'description', 'course', 'upload_date', 'file_type', 'created_at', 'updated_at']
        read_only_fields = ['upload_date', 'created_at', 'updated_at']

class StudyMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields = ['id', 'title', 'content', 'course', 'material_type', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'course', 'tags', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] 