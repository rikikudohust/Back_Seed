from django.shortcuts import render
from rest_framework.decorators import action
from .models import User,Teacher
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics,status
from django.http import Http404
import jwt

class UserView(APIView):
    def post(self,request,format=None):
        mydata = request.data
        email = mydata.data['email']
        password = mydata.data['password']
        user = User.objects.filter(email=email)
        if user is not None:
            if user.check_password(password):
                return Response(data=mydata,status=status.HTTP_200_OK)
            else:
                return Response("Password is not correct!")



