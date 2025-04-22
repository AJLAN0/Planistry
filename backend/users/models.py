from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom user model for the academic management platform.
    """
    email = models.EmailField(_('email address'), unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    institution = models.CharField(max_length=100, blank=True)
    major = models.CharField(max_length=100, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    
    # Study preferences
    preferred_study_time = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def __str__(self):
        return self.email
        
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email
        
class UserPreferences(models.Model):
    """
    Detailed user preferences for study habits and notifications.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='detailed_preferences')
    daily_study_goal = models.IntegerField(default=120)  # in minutes
    weekly_study_goal = models.IntegerField(default=600)  # in minutes
    preferred_study_duration = models.IntegerField(default=45)  # in minutes
    preferred_break_duration = models.IntegerField(default=15)  # in minutes
    reminder_frequency = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('custom', 'Custom'),
        ],
        default='daily'
    )
    intensity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
        ],
        default='low'
    )
    
    study_reminders_enabled = models.BooleanField(default=True)
    deadline_reminders_enabled = models.BooleanField(default=True)
    assessment_reminders_enabled = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('user preferences')
        verbose_name_plural = _('user preferences')
        
    def __str__(self):
        return f"{self.user.email}'s preferences"
