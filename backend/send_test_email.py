import os
import django
from django.core.mail import send_mail

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')
django.setup()

# Send test email
subject = 'Test Email from Planistry'
message = 'This is a test email sent from the Planistry application.'
from_email = 'planistry.info@gmail.com'
recipient_list = ['aj0ly.hd@gmail.com']

try:
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {str(e)}") 