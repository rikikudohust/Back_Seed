from django.db.models import query
from django.shortcuts import render
from django.utils.translation import activate
from rest_framework.decorators import action, schema
from .models import User,Teacher,Student,Schedule,ScheduleDaily, Class
from rest_framework import serializers, viewsets
from rest_framework.views import APIView
from .serializers import TeacherSerializer, UserSerializer,StudentSerializer,ScheduleDailySerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics,status
import jwt,datetime


class LoginView(APIView):
    def post(self, request,format=None):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User is not found!!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'role':user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed ('Unauthenicated!')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed ('Unauthenicated!')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.filter(active=True)
    serializer_class = StudentSerializer


class StudentScheduleView(APIView):
    def get(self,request,pk,format=None):
        data= Student.objects.filter(pk=pk).values('schedule')
        schedule = data[0]['schedule']
        schedulelist = ScheduleDaily.objects.filter(schedule=schedule)
        mydata = ScheduleDailySerializer(schedulelist,many=True)
        return Response(data=mydata.data,status=status.HTTP_200_OK)

class TeacherView(viewsets.ModelViewSet):
    queryset = Teacher.objects.filter(active=True)
    serializer_class = TeacherSerializer

class TeacherScheduleView(APIView):
    def get(self, request, pk, format=None):
        data  = Teacher.objects.filter(pk=pk).values('Class')
        classID = data[0]['Class']
        scheduleQuerySet = Class.objects.filter(pk=classID).values('schedule')
        scheduleId = scheduleQuerySet[0]['schedule']
        schedulelist = ScheduleDaily.objects.filter(schedule=scheduleId)
        print(schedulelist)
        mydata = ScheduleDailySerializer(schedulelist,many=True)
        return Response(data=mydata.data, status=status.HTTP_200_OK)
    

class TeacherSchdeduleDetailView(APIView):
    def get_object(self, pk, id):
        teacher  = Teacher.objects.filter(pk=pk).values('Class')
        classID = teacher[0]['Class']
        scheduleQuerySet = Class.objects.filter(pk=classID).values('schedule')
        scheduleId = scheduleQuerySet[0]['schedule']
        scheduleDetail = ScheduleDaily.objects.filter(schedule=scheduleId,name=id)
        return scheduleDetail

    def get(self, request, pk, id, format=None):
        scheduleDetails = self.get_object(pk, id)
        serializer_schedule = ScheduleDailySerializer(scheduleDetails, many=True)
        print(serializer_schedule.data)
        return Response(status=status.HTTP_200_OK)


        











