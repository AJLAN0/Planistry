from django.contrib import admin
from .models import Semester, Course, Assignment

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'start_date', 'end_date', 'is_active', 'created_at')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('name', 'user__email', 'user__username')
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'is_active')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'semester', 'instructor', 'credits', 'status', 'current_grade')
    list_filter = ('status', 'semester', 'credits')
    search_fields = ('code', 'name', 'instructor', 'semester__name')
    ordering = ('semester', 'code')
    
    fieldsets = (
        (None, {
            'fields': ('semester', 'code', 'name', 'instructor', 'credits')
        }),
        ('Details', {
            'fields': ('description', 'schedule')
        }),
        ('Status', {
            'fields': ('status', 'current_grade', 'target_grade')
        }),
    )

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'assignment_type', 'status', 'score', 'weight')
    list_filter = ('status', 'assignment_type', 'due_date', 'course')
    search_fields = ('title', 'description', 'course__name', 'course__code')
    ordering = ('due_date',)
    date_hierarchy = 'due_date'
    
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'description')
        }),
        ('Details', {
            'fields': ('assignment_type', 'due_date', 'weight')
        }),
        ('Status', {
            'fields': ('status', 'score')
        }),
    )
