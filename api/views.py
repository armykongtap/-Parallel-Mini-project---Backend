from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework import viewsets, filters

from .serializers import UserSerializer, GroupSerializer

from user.models import User
from group.models import Group


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

class GroupViewSet(viewsets.ModelViewSet) :
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def create(self, request, *args, **kwargs) :
        data = {}
        user_id = User.objects.filter(user_name=request.data['user_name']).values_list('user_id', flat=True)[0]
        text = request.data['group_name'] + "%_%" + request.data['user_name']
        print(text)
        data['group_name'] = text
        try :
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True) 
            self.perform_create(serializer)
            return HttpResponse("created")
        except Exception as e :
            return HttpResponseBadRequest(str(e))

class JoinViewSet(viewsets.ModelViewSet) :
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def create(self, request, *args, **kwargs) :
        data = {}
        try :
            group = Group.objects.filter(group_id=request.data['group_id'])
            user_id = User.objects.filter(user_name=request.data['user_name'])[0]
            data['user_id'] = user_id
            data['group_id'] = group[0]
            GroupSerializer.update(self, group, validated_data=data)
            return HttpResponse("joined")
        except Exception as e :
            return HttpResponseBadRequest(str(e))

class GetUserViewSet(viewsets.ModelViewSet) :
    serializer_class = UserSerializer

    def get_queryset(self) :
        user = User.objects.filter(user_name=self.request.data['user_name'])
        return user

class DeleteGroupViewSet(viewsets.ModelViewSet) :
    def create(self, request, *args, **kwargs) :
        username = request.data['user_name']
        gid = request.data['group_id']

        #Check if user is in the group
        usergroup = User.objects.filter(user_name=username).values_list('user_group', flat=True)
        if gid not in usergroup :
            return HttpResponseBadRequest("User is not in this group / Group does not exist!")

        try :
            Group.objects.get(group_id=gid).delete()
            return HttpResponse("deleted")
        except Exception as e :
            return HttpResponseBadRequest(str(e))

class LeaveGroupViewSet(viewsets.ModelViewSet) :
    def create(self, request, *args, **kwargs) :
        username = request.data['user_name']
        gid = request.data['group_id']

        #Check if user is in the group
        usergroup = User.objects.filter(user_name=username).values_list('user_group', flat=True)
        if gid not in usergroup :
            return HttpResponseBadRequest("User is not in this group / Group does not exist!")

        try :
            user = User.objects.get(user_name=username)
            user.user_group.remove(gid)
            return HttpResponse("left the group")
        except Exception as e :
            return HttpResponseBadRequest(str(e))