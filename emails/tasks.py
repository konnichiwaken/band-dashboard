from celery import shared_task

from .models import Email
from .utils import EmailServer


@shared_task
def send_unsent_emails():
    emails = Email.objects.filter(is_sent=False)
    email_server = EmailServer()
    for email in emails:
        email_server.send_email(email.recipient, email.body, email.subject)
        email.is_sent = True
        email.save()

    email_server.tear_down()