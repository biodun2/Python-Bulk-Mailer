from django.db import models

class MailDatas(models.Model):
    sender_email = models.CharField(max_length=30)
    sender_subject = models.CharField(max_length=1000)
    file = models.FileField(upload_to="mails")
    time = models.DateTimeField(auto_now_add=True)
    class Meta:
        get_latest_by = "file"
        ordering = ["-time"]
