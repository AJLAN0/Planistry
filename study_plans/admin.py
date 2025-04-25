from django.contrib import admin
from .models import StudyPlan, StudySession, StudyTask, Progress, Goal

@admin.register(StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'user', 'start_date', 'end_date', 'status', 'total_study_hours')
    list_filter = ('status', 'start_date', 'end_date', 'course')
    search_fields = ('title', 'description', 'course__name', 'course__code', 'user__email')
    ordering = ('-created_at',)
    date_hierarchy = 'start_date'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'course', 'title', 'description')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'total_study_hours')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'study_plan', 'start_time', 'end_time', 'duration')
    list_filter = ('start_time', 'study_plan')
    search_fields = ('topic', 'notes', 'study_plan__title')
    ordering = ('-start_time',)
    date_hierarchy = 'start_time'
    
    fieldsets = (
        (None, {
            'fields': ('study_plan', 'topic', 'notes')
        }),
        ('Timing', {
            'fields': ('start_time', 'end_time', 'duration')
        }),
    )
    
    readonly_fields = ('duration',)

@admin.register(StudyTask)
class StudyTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'study_plan', 'due_date', 'priority', 'status', 'estimated_duration')
    list_filter = ('status', 'priority', 'due_date', 'study_plan')
    search_fields = ('title', 'description', 'study_plan__title')
    ordering = ('due_date', 'priority')
    date_hierarchy = 'due_date'
    
    fieldsets = (
        (None, {
            'fields': ('study_plan', 'title', 'description')
        }),
        ('Task Details', {
            'fields': ('due_date', 'estimated_duration', 'priority')
        }),
        ('Status', {
            'fields': ('status', 'completed_at', 'completed_by')
        }),
        ('Dependencies', {
            'fields': ('parent_task', 'prerequisites')
        }),
    )
    
    readonly_fields = ('completed_at',)

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'study_plan', 'progress_percentage', 'total_study_time', 'completed_tasks', 'total_tasks')
    list_filter = ('last_activity', 'user', 'study_plan')
    search_fields = ('user__email', 'study_plan__title')
    ordering = ('-last_activity',)
    date_hierarchy = 'last_activity'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'study_plan')
        }),
        ('Progress Metrics', {
            'fields': ('total_study_time', 'completed_tasks', 'total_tasks', 'progress_percentage')
        }),
        ('Activity', {
            'fields': ('last_activity',)
        }),
    )
    
    readonly_fields = ('last_activity',)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'study_plan', 'status', 'due_date')
    list_filter = ('status', 'due_date', 'study_plan')
    search_fields = ('title', 'description', 'study_plan__title')
    ordering = ('due_date',)
    date_hierarchy = 'due_date'
    
    fieldsets = (
        (None, {
            'fields': ('study_plan', 'title', 'description')
        }),
        ('Status', {
            'fields': ('status', 'due_date')
        }),
    )
