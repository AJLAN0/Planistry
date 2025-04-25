from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models import Course, Assignment
from users.models import User
from django.conf import settings

class StudyPlan(models.Model):
    """
    Represents a study plan for a course.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='study_plans')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='study_plans')
    
    # Study plan settings
    start_date = models.DateField()
    end_date = models.DateField()
    total_study_hours = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Study plan status
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('study plan')
        verbose_name_plural = _('study plans')
        
    def __str__(self):
        return f"{self.course.code} - {self.title} - {self.user.username}"

class StudySession(models.Model):
    """
    Represents a planned or completed study session.
    """
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, related_name='study_sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.FloatField(help_text='Duration in hours')
    topic = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.topic} - {self.study_plan.title}"

class StudyTask(models.Model):
    """
    Represents a specific task within a study plan.
    """
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Task timing
    due_date = models.DateTimeField()
    estimated_duration = models.IntegerField(help_text='Estimated duration in minutes')
    
    # Task priority
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Task status
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('deferred', 'Deferred'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    
    # Task relationships
    parent_task = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subtasks')
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='dependent_tasks')
    
    # Task completion
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='completed_tasks')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['due_date', 'priority']
        verbose_name = _('study task')
        verbose_name_plural = _('study tasks')
        
    def __str__(self):
        return f"{self.study_plan.course.code} - {self.title}"

class Progress(models.Model):
    """
    Tracks progress for study plans and tasks.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_records')
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, related_name='progress_records')
    
    # Progress metrics
    total_study_time = models.IntegerField(default=0, help_text='Total study time in minutes')
    completed_tasks = models.IntegerField(default=0)
    total_tasks = models.IntegerField(default=0)
    
    # Progress status
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    last_activity = models.DateTimeField(auto_now=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_activity']
        verbose_name = _('progress')
        verbose_name_plural = _('progress records')
        
    def __str__(self):
        return f"{self.user.email} - {self.study_plan.course.code} Progress"

class Goal(models.Model):
    STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, related_name='goals')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.study_plan.title}"
