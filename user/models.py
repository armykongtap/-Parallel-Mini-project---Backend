from django.db import models
from group.models import Group
# from message.models import Message

class User(models.Model) :
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20)
    user_group = models.ManyToManyField(Group, null=True, blank=True)
    user_recent_message = models.ManyToManyField('message.Message', null=True, blank=True)

    def __str__(self) :
        return self.user_name