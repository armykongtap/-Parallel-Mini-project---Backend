from django.db import models
from user.models import User
from group.models import Group

class Message(models.Model) :
    msg_id = models.AutoField(primary_key=True)
    msg_text = models.CharField(max_length=100)
    msg_sender = models.ForeignKey(User, related_name='message_sender', on_delete=models.CASCADE)
    msg_group = models.ForeignKey(Group, related_name='group', on_delete=models.CASCADE)
    msg_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.msg_text

    class Meta :
        ordering = ('msg_timestamp',)

# Message - msgID, msg, senderID, groupID, timestamp
# Group - groupID, userID
# User - userID, groupID, recentMessage