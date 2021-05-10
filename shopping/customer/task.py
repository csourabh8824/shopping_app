from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_registration_mail(data):
    username = data['username']
    msg = f'Dear, {username} You have successfully registered. Now you can login'
    send_mail('Registration Successfull', msg,
              "sochoudhary@deqode.com", [data['email']],fail_silently=False
              )
    return None