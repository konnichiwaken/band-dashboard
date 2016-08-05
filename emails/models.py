from django.db import models

class Email(models.Model):
    recipient = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_sent = models.BooleanField(default=False)
