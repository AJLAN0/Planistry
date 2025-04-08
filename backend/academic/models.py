from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User

class Semester(models.Model):
    """
    Represents an academic semester.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='semesters')
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = _('semester')
        verbose_name_plural = _('semesters')
        
    def __str__(self):
        return f"{self.name} ({self.start_date.year})"
        
class Course(models.Model):
    """
    Represents an academic course within a semester.
    """
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    instructor = models.CharField(max_length=100)
    credits = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField(blank=True)
    
    # Schedule
    schedule = models.JSONField(default=dict)  # Store class times and locations
    
    # Course status
    COURSE_STATUS = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('planned', 'Planned'),
    ]
    status = models.CharField(max_length=20, choices=COURSE_STATUS, default='active')
    
    # Grade tracking
    current_grade = models.CharField(max_length=2, blank=True)
    target_grade = models.CharField(max_length=2, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = _('course')
        verbose_name_plural = _('courses')
        unique_together = ['semester', 'code']
        
    def __str__(self):
        return f"{self.code} - {self.name}"
        
class Assignment(models.Model):
    """
    Represents a course assignment or assessment.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text='Percentage weight in final grade')
    
    # Assignment type
    ASSIGNMENT_TYPES = [
        ('homework', 'Homework'),
        ('quiz', 'Quiz'),
        ('exam', 'Exam'),
        ('project', 'Project'),
        ('paper', 'Paper'),
        ('presentation', 'Presentation'),
        ('other', 'Other'),
    ]
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPES)
    
    # Status tracking
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['due_date']
        verbose_name = _('assignment')
        verbose_name_plural = _('assignments')
        
    def __str__(self):
        return f"{self.course.code} - {self.title}"
        
    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.due_date < timezone.now() and self.status not in ['submitted', 'graded']
