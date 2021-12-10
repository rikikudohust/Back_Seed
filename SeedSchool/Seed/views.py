from django.shortcuts import render
from rest_framework.decorators import action
from .models import User,Teacher,Student,Schedule,ScheduleDaily,Class,GeneralActivities,ResigterActivities,Attended

from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import (UserSerializer,StudentSerializer,ScheduleDailySerializer,TeacherSerializer,ClassSerializer,GeneralActivitiesSerializer,RegisterActivitiesSerializer,
                        AttendSerializer
                          )

from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics,status
from rest_framework.parsers import MultiPartParser, FormParser
import jwt,datetime

class RegisterView(APIView):

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            role = serializer.data['role']
            print('1')
            if (role == 2 ):
                student_data = {"user":serializer.data['id'],
                                "email":serializer.data['email']
                                }
                student_serializer = StudentSerializer(data=student_data)
                if student_serializer.is_valid():
                    student_serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
            elif (role == 1 ):
                teacher_data = {"user":serializer.data['id'],
                                "email":serializer.data['email']
                                }
                teacher_serializer = TeacherSerializer(data=teacher_data)
                if teacher_serializer.is_valid():
                    teacher_serializer.save()
                    return Response(data=serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)




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
        pass

class TeacherView(viewsets.ModelViewSet):
    queryset = Teacher.objects.filter(active=True)
    serializer_class = TeacherSerializer

class TeacherScheduleView(APIView):
    def get_object(self, pk):
        classInstance = Class.objects.filter(teacher=pk).first()
        scheduleInstance = Schedule.objects.filter(classes=classInstance.id).first()      
        return scheduleInstance

    def get(self, request, pk, format=None):
        scheduleInstance = self.get_object(pk)
        if scheduleInstance == None:
            return Response(data={'message':"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        schedule_serializer = ScheduleSerializer(scheduleInstance)
        scheduleId = schedule_serializer.data['classes']
        scheduleDailyList = ScheduleDaily.objects.filter(schedule=scheduleId)
        serializer = ScheduleDailySerializer(scheduleDailyList, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk, format=None):
        pass
    
class TeacherSchdeduleDailyView(APIView):
    def get_object(self, pk, id):
        classInstance = Class.objects.filter(teacher=pk).first()
        scheduleInstance = Schedule.objects.filter(classes=classInstance.id).first()      
        schedule_serializer = ScheduleSerializer(scheduleInstance)
        scheduleId = schedule_serializer.data['classes']
        scheduleDailyInstance = ScheduleDaily.objects.filter(schedule = scheduleId)
        return scheduleDailyInstance

    def get(self, request, pk, id, format=None):
        scheduleDailyInstance = self.get_object(pk, id)
        serializer = ScheduleDailySerializer(scheduleDailyInstance, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk, format=None):
        pass

#Lay thong tin lop cua giao vien
class TeacherClassView(APIView):
    def get_object(self, pk):
        classInstance = Class.objects.filter(teacher=pk).first()
        return classInstance

    def get(self, request, pk, format=None):
        classInstance = self.get_object(pk)
        if classInstance:
            classInstance = self.get_object(pk)
            serializer = ClassSerializer(classInstance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'message':'Not Found'},status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk, format=None):
        classInstance = self.get_object(pk)
        if not classInstance == None:
            return Response(data= {'message':"Class Exited"}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        data['teacher'] = pk
        serializer = ClassSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            schedule_data = {"classes": serializer.data['id']}
            schedule_serializer = ScheduleSerializer(data=schedule_data)
            if schedule_serializer.is_valid():
                schedule_serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(schedule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    def put(self, request, pk, format=None):
        classInstance = self.get_object(pk)
        serializer = ClassSerializer(classInstance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        classInstance = self.get_object(pk)
        classInstance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TeacherStudentView(APIView):
    def get_object(self, pk):
        studentListInstance = Student.objects.filter(idteacher=pk)
        return studentListInstance
    
    def get(self, request, pk, format=None):
        studentListInstance = self.get_object(pk)
        serializer = StudentSerializer(studentListInstance, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk, format=None):
        data = request.data
        classInstance = Class.objects.filter(teacher=pk).first()
        scheduleInstance = Schedule.objects.filter(pk=classInstance.id).first()
        studentInstance = Student.objects.filter(email=data['email']).first()
        serializer = StudentSerializer(studentInstance)
        data = serializer.data
        data['classes'] = classInstance.id
        data['schedule'] = classInstance.id
        print(data)
        serializer_student = StudentSerializer(studentInstance, data=data)
        if serializer_student.is_valid():
            return Response(data=serializer_student.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer_student.errors,status=status.HTTP_400_BAD_REQUEST)
        
class StudentAttendanceView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, pk, format = None):
        data = request.data
        data['id'] = pk
        print(data)
        serializer = AttendSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        


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

class RegisterActivitiesView(APIView):
    def post(self,request,pk,id,format=None):
        serializer = RegisterActivitiesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_200_OK)

# class StudentAbsentView(generics.CreateAPIView,generics.ListAPIView):
    # queryset = Attended.objects.all()
    # serializer_class = AttendSerializer

class StudentAbsentView(APIView):
    def post(self,request,pk,format=None):
        serialzer_data = {
                "student": pk,
                "absent": "true"
            }

        serializer = AttendSerializer(data=serialzer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

















