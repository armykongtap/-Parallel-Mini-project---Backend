from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import UserSerializer

from user.models import User


class LoginViewSet(viewsets.ModelViewSet) :
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs) :
        data = {}
        username = request.data['user_name']
        data['user_name'] = username

        #Register Case
        if not User.objects.filter(user_name=username).exists() :
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        #Retrieve Existing User
        user = User.objects.filter(user_name=username)
        jsondata = {}
        jsondata['user_id'] = user.values_list('user_id', flat=True)[0]
        jsondata['user_name'] = user.values_list('user_name', flat=True)[0]
        return JsonResponse(jsondata)