from django.db.models import query
from django.shortcuts import get_object_or_404, render
from django.utils.translation import activate
from rest_framework.decorators import action, schema
from .models import User,Teacher,Student,Schedule,ScheduleDaily, Class
from rest_framework import serializers, viewsets
from rest_framework.views import APIView
from .serializers import ClassSerializer, TeacherSerializer, UserSerializer,StudentSerializer,ScheduleDailySerializer
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
        pass

class TeacherView(viewsets.ModelViewSet):
    queryset = Teacher.objects.filter(active=True)
    serializer_class = TeacherSerializer

class TeacherScheduleView(APIView):
    def get(self, request, pk, format=None):
        pass
    
    def post(self, request, pk, format=None):
        pass
    
class TeacherSchdeduleDailyView(APIView):
    def get_object(self, pk, id):
        pass

    def get(self, request, pk, id, format=None):
        pass
    
    def post(self, request, pk, format=None):
        pass

#Lay thong tin lop cua giao vien
class TeacherClassView(APIView):
    def get_object(self, pk):
        classInstance = Class.objects.get(teacher=pk)
        return classInstance

    def get(self, request, pk, format=None):
        classInstance = self.get_object(pk)
        if classInstance:
            classInstance = self.get_object(pk)
            serializer = ClassSerializer(classInstance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'message':'Not Found'},status=status.HTTP_404_NOT_FOUND)
    #Create new class (create schedule for class)
    def post(self, request, pk, format=None):
        classInstance = self.get_object(pk)
        serializer = ClassSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherStudentView(APIView):
    def get_object(self, pk):
        studentInstance = Student.objects.filter(idteacher=pk)
        return studentInstance
    
    def get(self, request, pk, format=None):
        studentInstance = self.get_object(pk)
        serializer = StudentSerializer(studentInstance, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        











