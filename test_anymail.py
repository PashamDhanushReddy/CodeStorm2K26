import os
import django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

# Setup minimal settings to test anymail
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codestorm_project.settings')
django.setup()

def send_test_email():
    print("Testing anymail with Brevo...")
    msg = EmailMultiAlternatives(
        "Test Subject",
        "Test Body",
        settings.DEFAULT_FROM_EMAIL,
        ["codestorm2k26v2@gmail.com"] # send to self
    )
    
    try:
        msg.send(fail_silently=False)
        print("Success! Email sent.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    send_test_email()
