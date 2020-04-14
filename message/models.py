from django.db import models

class Message(models.Model) :
    msgID = models.AutoField(primary_key=True)
    msg = models.CharField(max_length=100)
    sender = models.ForeignKey(User, related_name='message_sender', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='group', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.msg

    class Meta :
        ordering = ('timestamp',)

# Message - msgID, msg, senderID, groupID, timestamp
# Group - groupID, userID
# User - userID, groupID, recentMessage