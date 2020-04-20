from rest_framework import fields, serializers, status
from rest_framework.response import Response
from django.contrib.auth.validators import UnicodeUsernameValidator
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework.validators import UniqueValidator
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin, NestedUpdateMixin

# Import App Models
from user.models import User
from group.models import Group
from message.models import Message

class GroupSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Group
        fields = '__all__'

    def create(self, validated_data) :
        text = validated_data.pop('group_name').split("%_%")
        newgroup = Group.objects.create(group_name=text[0])
        user = User.objects.get(user_name=text[1])
        newgroup.save()
        user.user_group.add(newgroup)
        return newgroup

    def update(self, instance, validated_data) :
        user = validated_data.pop('user_name')
        user.user_group.add(validated_data.pop('group_id'))

class MessageSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Message
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer) :
    user_group = GroupSerializer(many=True, required=False)
    user_recent_message = MessageSerializer(many=True, required=False)

    class Meta :
        model = User
        fields = '__all__'

    def create(self, validated_data) :
        newuser = User.objects.create(user_name=validated_data.pop('user_name'))
        newuser.save()
        return newuser