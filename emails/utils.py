import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from django.conf import settings

from emails.models import Email


class EmailServer(object):

    def __init__(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)

    def tear_down(self):
        self.server.quit()

    def send_email(self, recipient, message, subject):
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_USERNAME
        msg['To'] = recipient
        msg['Subject'] = subject
        body = message
        msg.attach(MIMEText(body, 'plain'))

        text = msg.as_string()
        self.server.sendmail(settings.EMAIL_USERNAME, recipient, text)
