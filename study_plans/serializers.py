from rest_framework import serializers
from .models import StudyPlan, StudySession, StudyTask, Progress, Goal
from users.serializers import UserSerializer
from academic.serializers import CourseSerializer


class StudySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySession
        fields = [
            'id', 'study_plan', 'start_time', 'end_time', 'duration', 'topic',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at')


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = [
            'id', 'title', 'description', 'study_plan', 'status', 'due_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at')


class StudyTaskSerializer(serializers.ModelSerializer):
    parent_task = serializers.PrimaryKeyRelatedField(read_only=True)
    prerequisites = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    completed_by = UserSerializer(read_only=True)

    class Meta:
        model = StudyTask
        fields = [
            'id', 'study_plan', 'title', 'description', 'due_date', 'estimated_duration',
            'priority', 'status', 'parent_task', 'prerequisites',
            'completed_at', 'completed_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at')


class ProgressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    study_plan = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Progress
        fields = [
            'id', 'user', 'study_plan', 'total_study_time', 'completed_tasks',
            'total_tasks', 'progress_percentage', 'last_activity', 'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at')


class StudyPlanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    study_sessions = StudySessionSerializer(many=True, read_only=True)
    tasks = StudyTaskSerializer(many=True, read_only=True)
    goals = GoalSerializer(many=True, read_only=True)
    progress_records = ProgressSerializer(many=True, read_only=True)

    class Meta:
        model = StudyPlan
        fields = [
            'id', 'course', 'title', 'description', 'user',
            'start_date', 'end_date', 'total_study_hours', 'status',
            'created_at', 'updated_at',
            'study_sessions', 'tasks', 'goals', 'progress_records'
        ]
        read_only_fields = ('created_at', 'updated_at')
