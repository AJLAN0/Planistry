from django.contrib import admin
from .models import Notification, NotificationPreference, NotificationLog

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'priority', 'is_read', 'scheduled_for', 'created_at')
    list_filter = ('notification_type', 'priority', 'is_read', 'is_dismissed', 'scheduled_for')
    search_fields = ('title', 'message', 'user__email')
    ordering = ('-created_at',)
    date_hierarchy = 'scheduled_for'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'message')
        }),
        ('Classification', {
            'fields': ('notification_type', 'priority')
        }),
        ('Related Content', {
            'fields': ('content_type', 'object_id')
        }),
        ('Status', {
            'fields': ('is_read', 'is_dismissed', 'read_at')
        }),
        ('Scheduling', {
            'fields': ('scheduled_for', 'expires_at')
        }),
    )
    
    readonly_fields = ('read_at',)

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications', 'push_notifications', 'email_frequency')
    list_filter = ('email_notifications', 'push_notifications', 'email_frequency')
    search_fields = ('user__email',)
    
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Email Settings', {
            'fields': ('email_notifications', 'email_frequency')
        }),
        ('Push Notifications', {
            'fields': ('push_notifications', 'quiet_hours_start', 'quiet_hours_end')
        }),
        ('Notification Types', {
            'fields': (
                'notify_assignment_due',
                'notify_study_session',
                'notify_quiz_available',
                'notify_progress_updates'
            )
        }),
        ('Reminder Settings', {
            'fields': ('reminder_advance_time', 'reminder_frequency')
        }),
    )

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('notification', 'status', 'delivery_method', 'attempt_count', 'last_attempt')
    list_filter = ('status', 'delivery_method', 'last_attempt')
    search_fields = ('notification__title', 'error_message')
    ordering = ('-created_at',)
    date_hierarchy = 'last_attempt'
    
    fieldsets = (
        (None, {
            'fields': ('notification', 'delivery_method')
        }),
        ('Delivery Status', {
            'fields': ('status', 'attempt_count', 'last_attempt')
        }),
        ('Error Information', {
            'fields': ('error_message',)
        }),
    )
    
    readonly_fields = ('last_attempt',)
