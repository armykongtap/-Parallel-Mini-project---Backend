from rest_framework import fields, serializers, status
from rest_framework.response import Response
from django.contrib.auth.validators import UnicodeUsernameValidator
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework.validators import UniqueValidator
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin, NestedUpdateMixin

# Import App Models
from user.models import User

class UserSerializer(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = '__all__'

    def create(self, validated_data) :
        name = validated_data.pop('user_name')
        newuser = User.objects.create(user_name=name)
        newuser.save()
        return newuser