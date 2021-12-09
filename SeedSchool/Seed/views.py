from django.shortcuts import render
from rest_framework.decorators import action
from .models import User,Teacher,Student,Schedule,ScheduleDaily,Class,GeneralActivities

from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import UserSerializer,StudentSerializer,ScheduleDailySerializer,TeacherSerializer,ClassSerializer,GeneralActivitiesSerializer
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



class TeacherView(viewsets.ModelViewSet):
    queryset = Teacher.objects.filter(active=True)
    serializer_class = TeacherSerializer


class StudentScheduleView(APIView):
    def get(self,request,pk,format=None):
        data= Student.objects.filter(pk=pk).values('schedule')
        schedule = data[0]['schedule']
        schedulelist = ScheduleDaily.objects.filter(schedule=schedule)
        mydata = ScheduleDailySerializer(schedulelist,many=True)
        return Response(data=mydata.data,status=status.HTTP_200_OK)


class StudentScheduleDetailView(APIView):
    def get_object(self,pk,id,format=None):
        data = Student.objects.filter(pk=pk).values('schedule')
        schedule = data[0]['schedule']
        scheduleDetail = ScheduleDaily.objects.filter(schedule=schedule,name=id)
        return scheduleDetail

    def get(self,request,pk,id,format=None):
        scheduleDetails = self.get_object(pk,id)
        serializer = ScheduleDailySerializer(scheduleDetails,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class StudentTeacherDetailView(APIView):
    def get_object(self,pk,format=None):
        data = Student.objects.filter(pk=pk).values('idteacher')
        print(data)
        teacher = data[0]['idteacher']
        print(teacher)
        teacherdetail = Teacher.objects.filter(user=teacher).first()
        return teacherdetail
    def get(self,request,pk,format=None):
        teacherdetail = self.get_object(pk)
        mydata = TeacherSerializer(teacherdetail)
        print(mydata)
        return Response(data=mydata.data,status=status.HTTP_200_OK)

class ActivitiesView(viewsets.ModelViewSet):
    queryset = GeneralActivities.objects.all()
    serializer_class = GeneralActivitiesSerializer

class ClassDetailView(APIView):
    def get(self,request,pk):
        student = Student.objects.filter(Class=pk)
        print(student)
        mydata = StudentSerializer(student,many=True)
        return Response(data=mydata.data,status=status.HTTP_200_OK)













