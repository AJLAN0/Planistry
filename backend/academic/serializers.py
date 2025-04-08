from rest_framework import serializers
from .models import Semester, Course, Assignment

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'due_date', 'status', 'course', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class CourseSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'credits', 'semester', 'schedule', 'instructor', 'assignments', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class SemesterSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Semester
        fields = ['id', 'name', 'start_date', 'end_date', 'is_active', 
                 'courses', 'created_at', 'updated_at']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add any computed fields or format dates
        data['start_date'] = instance.start_date.strftime('%Y-%m-%d')
        data['end_date'] = instance.end_date.strftime('%Y-%m-%d')
        return data