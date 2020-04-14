from django.db import models

class Message(models.Model):
    msgId = models.AutoField(primary_key=True)
    msg = models.CharField(max_length=100)
