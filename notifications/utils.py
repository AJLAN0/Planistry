from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Notification, NotificationLog

def send_email_notification(notification, template_name=None):
    """
    Send an email notification to a user.
    
    Args:
        notification (Notification): The notification object to send
        template_name (str, optional): The name of the email template to use
    """
    try:
        # Get user's notification preferences
        preferences = notification.user.notificationpreference_set.first()
        if not preferences or not preferences.email_notifications:
            return False

        subject = notification.title
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = notification.user.email

        # If template provided, use it
        if template_name:
            context = {
                'user': notification.user,
                'notification': notification,
                'site_name': settings.SITE_NAME,
            }
            html_content = render_to_string(f'notifications/email/{template_name}.html', context)
            text_content = strip_tags(html_content)
        else:
            # Use notification message directly
            text_content = notification.message
            html_content = notification.message.replace('\n', '<br>')

        # Create email message
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[to_email]
        )
        
        # Attach HTML content
        email.attach_alternative(html_content, "text/html")
        
        # Send email
        email.send()

        # Log the successful notification
        NotificationLog.objects.create(
            notification=notification,
            delivery_method='email',
            status='sent'
        )
        
        return True

    except Exception as e:
        # Log the failed notification
        NotificationLog.objects.create(
            notification=notification,
            delivery_method='email',
            status='failed',
            error_message=str(e)
        )
        return False 