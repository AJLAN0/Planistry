from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from users.models import User
from django.conf import settings

class Notification(models.Model):
    """
    Represents a notification for a user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    
    # Notification type
    NOTIFICATION_TYPES = (
        ('assignment', 'Assignment'),
        ('study_session', 'Study Session'),
        ('quiz', 'Quiz'),
        ('progress', 'Progress'),
        ('system', 'System'),
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    
    # Priority levels
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    
    # Generic foreign key to related object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')
    
    # Notification status
    is_read = models.BooleanField(default=False)
    is_dismissed = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Scheduling
    scheduled_for = models.DateTimeField()
    expires_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']

class NotificationPreference(models.Model):
    """
    Stores user preferences for notifications.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email preferences
    email_notifications = models.BooleanField(default=True)
    email_frequency = models.CharField(
        max_length=20,
        choices=[
            ('immediate', 'Immediate'),
            ('daily', 'Daily Digest'),
            ('weekly', 'Weekly Digest'),
        ],
        default='immediate'
    )
    
    # Push notification preferences
    push_notifications = models.BooleanField(default=True)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    
    # Notification types to receive
    notify_assignment_due = models.BooleanField(default=True)
    notify_study_session = models.BooleanField(default=True)
    notify_quiz_available = models.BooleanField(default=True)
    notify_progress_updates = models.BooleanField(default=True)
    
    # Reminder settings
    reminder_advance_time = models.IntegerField(default=24, help_text='Hours before deadline')
    reminder_frequency = models.CharField(
        max_length=20,
        choices=[
            ('once', 'Once'),
            ('daily', 'Daily'),
            ('custom', 'Custom'),
        ],
        default='once'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('notification preference')
        verbose_name_plural = _('notification preferences')
        
    def __str__(self):
        return f"{self.user.email}'s notification preferences"

class NotificationLog(models.Model):
    """
    Logs notification delivery attempts and status.
    """
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='delivery_logs')
    
    # Delivery status
    DELIVERY_STATUS = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('delivered', 'Delivered'),
    ]
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS)
    
    # Delivery details
    delivery_method = models.CharField(max_length=50)  # e.g., 'email', 'push', 'sms'
    attempt_count = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('notification log')
        verbose_name_plural = _('notification logs')
        
    def __str__(self):
        return f"Delivery log for {self.notification}"
