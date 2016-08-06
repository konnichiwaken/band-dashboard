import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from django.conf import settings

from .models import Email


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


def send_substitution_form_email(event, requestee, requester):
    from .tasks import send_unsent_emails

    msg = """
    Hello, {}!

    {} has requested a substitution for {} at {}. Please log on to DUMBDash to either accept or decline the substitution request.

    Sincerely,
    SG
    """.format(
        requestee.account.first_name,
        requester.account.get_full_name(),
        event.title,
        event.time.strftime("%I:%M %p on %B %d, %Y"))
    subject = "{} has requested a substitution".format(requester.account.get_full_name())
    Email.objects.create(recipient=requestee.account.email, subject=subject, body=msg)
    send_unsent_emails.apply_async(())

