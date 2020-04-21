# python manage.py shell
# then copy this file

from user.models import User
from group.models import Group
from message.models import Message

for i in range(1, 11):
    u = User(user_name="user"+str(i))
    g = Group(group_name="group"+str(i))
    m = Message(msg_text="message "+str(i)+" from user "+str(i) +
                " to group "+str(i), msg_sender=u, msg_group=g)
    u.save()
    g.save()
    m.save()
