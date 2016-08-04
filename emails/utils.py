import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from django.conf import settings


def send_email(recipient, message, subject):
    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_USERNAME
    msg['To'] = recipient
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)

    text = msg.as_string()
    server.sendmail(settings.EMAIL_USERNAME, recipient, text)
    server.quit()
