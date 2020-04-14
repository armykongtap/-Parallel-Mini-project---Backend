from django.db import models
# from user.models import User

class Group(models.Model) :
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=20)
    group_users = models.ManyToManyField('user.User', related_name='users_in_group')

    def __str__(self) :
        return self.group_name