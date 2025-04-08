from rest_framework import serializers
from .models import StudyPlan, StudySession, Goal

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'status', 'due_date', 'study_plan', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class StudySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySession
        fields = ['id', 'start_time', 'end_time', 'duration', 'topic', 'notes', 'study_plan', 'created_at', 'updated_at']
        read_only_fields = ['duration', 'created_at', 'updated_at']
    
    def validate(self, data):
        if data.get('end_time') and data.get('start_time'):
            if data['end_time'] <= data['start_time']:
                raise serializers.ValidationError("End time must be after start time")
        return data
    
    def create(self, validated_data):
        if validated_data.get('end_time') and validated_data.get('start_time'):
            validated_data['duration'] = (validated_data['end_time'] - validated_data['start_time']).total_seconds() / 3600
        return super().create(validated_data)

class StudyPlanSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many=True, read_only=True)
    study_sessions = StudySessionSerializer(many=True, read_only=True)
    
    class Meta:
        model = StudyPlan
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'goals', 'study_sessions', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, data):
        if data.get('end_date') and data.get('start_date'):
            if data['end_date'] <= data['start_date']:
                raise serializers.ValidationError("End date must be after start date")
        return data 