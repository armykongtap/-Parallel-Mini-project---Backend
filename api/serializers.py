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

class UserSerializer(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = '__all__'

    def create(self, validated_data) :
        newuser = User.objects.create(user_name=validated_data.pop('user_name'))
        newuser.save()
        return newuser

class GroupSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Group
        fields = '__all__'
    
    def create(self, validated_data) :
        newgroup = Group.objects.create(group_name=validated_data.pop('group_name'))
        user = validated_data.pop('group_users')
        newgroup.group_users.set(user)
        newgroup.save()
        user[0].user_group.add(newgroup)
        return newgroup

    def update(self, instance, validated_data) :
        instance.group_users.add(validated_data.pop('user_name'))