from rest_framework import serializers
from .models import CourseFile, StudyMaterial, Note

class CourseFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    download_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CourseFile
        fields = ['id', 'title', 'description', 'course', 'category',
                  'file', 'filename', 'file_type', 'size', 'created_at', 'updated_at', 'download_url']
        read_only_fields = ['created_at', 'updated_at', 'size', 'filename', 'file_type', 'download_url']

    def create(self, validated_data):
        file_obj = validated_data.pop('file')
        file_content = file_obj.read()
        validated_data.update({
            'file': file_content,
            'filename': file_obj.name,
            'file_type': file_obj.name.split('.')[-1],
            'size': file_obj.size,
        })
        return super().create(validated_data)

    def get_download_url(self, obj):
        return f"/api/course-files/{obj.id}/download/"

class StudyMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
