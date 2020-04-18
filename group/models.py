from django.db import models

class Group(models.Model) :
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=20)

    def __str__(self) :
        return self.group_name