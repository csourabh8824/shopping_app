from celery import shared_task

from django.core.mail import send_mail

@shared_task
def send_order_mail(email,html_message):
    msg = f'Order successfully placed'
    send_mail('Order Placed', msg,
              "sochoudhary@deqode.com", [email],fail_silently=False,html_message=html_message
              )
    return None