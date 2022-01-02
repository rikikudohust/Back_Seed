from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.decorators import action
from .models import Menu, User,Teacher,Student,ScheduleDaily,Class,GeneralActivities,ResigterActivities,Attended, Task, ResigterActivities,Meal,Thank

from rest_framework import serializers, viewsets
from rest_framework.views import APIView
from .serializers import (UserSerializer,StudentSerializer,ScheduleDailySerializer,TeacherSerializer,ClassSerializer,GeneralActivitiesSerializer,RegisterActivitiesSerializer,
                        AttendSerializer, TaskSerializer, MenuSerializer,MealSerializer,AttendSerializer1,ThankSerializer)
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics,status
from rest_framework.parsers import MultiPartParser, FormParser
import jwt,datetime
from datetime import date
from django.contrib.auth.models import Group


###################### GROUP ############################
student_group, created = Group.objects.get_or_create(name='Student')
admin_group, created = Group.objects.get_or_create(name='Admin')
teacher_group, created = Group.objects.get_or_create(name='Teacher')


###################### USER VIEW ############################
class RegisterView(APIView):

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            role = serializer.data['role']
            if (role == 2 ):
                user = User.objects.filter(role=role).first()
                student_group.user_set.add(user)
                student_data = {"user":serializer.data['id'],
                                "email":serializer.data['email'],
                                "name" : serializer.data['username']
                                }
                student_serializer = StudentSerializer(data=student_data)
                if student_serializer.is_valid():
                    student_serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            elif (role == 1 ):
                user = User.objects.filter(role=role).first()
                teacher_group.user_set.add(user)
                teacher_data = {"user":serializer.data['id'],
                                "email":serializer.data['email'],
                                "name": serializer.data['username']
                                }
                teacher_serializer = TeacherSerializer(data=teacher_data)
                if teacher_serializer.is_valid():
                    teacher_serializer.save()
                    return Response(data=serializer.data,status=status.HTTP_201_CREATED)
            elif (role ==3 ):
                user = User.objects.filter(role=role).first()
                admin_group.user_set.add(user)
                admin_data = {"user": serializer.data['id'],
                                "email": serializer.data['email'],
                                "name": serializer.data['username']
                                }
                admin_serializer = TeacherSerializer(data=admin_data)
                if admin_serializer.is_valid():
                    admin_serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


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
            'jwt': token,
            'id':user.id,
            'role':user.role
        }
        return response

# class UserView(APIView):
#     def get(self,request):
#         token = request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed ('Unauthenicated!')
#         try:
#             payload = jwt.decode(token,'secret',algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed ('Unauthenicated!')
#         user = User.objects.filter(id=payload['id']).first()
#         serializer = UserSerializer(user)
#         return Response(serializer.data)


class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

"""
            ============================
           |        TEACHER VIEW        |
            ============================
"""


class TeacherView(APIView):
    def get(self,request,format=None):

        teacher = Teacher.objects.filter(active=True)
        serializer = TeacherSerializer(teacher,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class TeacherDetailView(APIView):
    def get_object(self,pk):
        return Teacher.objects.get(pk=pk)

    def get(self,request,pk,format=None):
        teacher = self.get_object(pk)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request,pk,format=None):
        teacher = self.get_object(pk)
        serializer = TeacherSerializer(teacher,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        teacher = self.get_object(pk)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TeacherScheduleView(APIView):
    def get_object(self, pk):
        classInstance = Class.objects.filter(teacher=pk).first()
        scheduleInstance = ScheduleDaily.objects.filter(classes=classInstance.id)      
        return scheduleInstance

    def get(self, request, pk, format=None):
        scheduleInstance = self.get_object(pk)
        if scheduleInstance == None:
            return Response(data={'message':"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        schedule_serializer = ScheduleDailySerializer(scheduleInstance, many=True)
        return Response(data=schedule_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk, format=None):
        classInstance = Class.objects.filter(teacher=pk).first()
        classId = classInstance.id
        data = request.data
        data['classes'] = classId
        serializer = ScheduleDailySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TeacherScheduleDetailView(APIView):
    def get_object(self, pk, id):
        classInstance = Class.objects.filter(teacher=pk).first()
        classId = classInstance.id
        scheduleDailyInstance = ScheduleDaily.objects.filter(classes=classId, name=id).first()
        taskList = Task.objects.filter(scheduleDaily= scheduleDailyInstance.id)
        return taskList

    def get(self, request, pk, id, format=None):
        taskList = self.get_object(pk, id)
        serializer = TaskSerializer(taskList, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk,id, format=None):
        classInstance = Class.objects.filter(teacher=pk).first()
        classId = classInstance.id
        scheduleDailyInstance = ScheduleDaily.objects.filter(classes=classId, name=id).first()
        data = request.data
        data['scheduleDaily'] = scheduleDailyInstance.id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
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
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
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
    
    def put(self, request, pk, format=None):
        data = request.data
        classInstance = Class.objects.filter(teacher=pk).first()
        studentInstance = Student.objects.filter(email=data['email']).first()
        if studentInstance == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(studentInstance)
        data = serializer.data
        data['classes'] = classInstance.id
        data['idteacher'] = pk
        serializer_student = StudentSerializer(studentInstance, data=data)
        if serializer_student.is_valid():
            serializer_student.save()
            return Response(data=serializer_student.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer_student.errors,status=status.HTTP_400_BAD_REQUEST)


class TeacherThankView(APIView):
    def post(self,request,pk,format=None):
        data = request.data
        data['teacher']=pk
        serializer = ThankSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get(self,request,pk,format=None):
        teacher = Thank.objects.filter(teacher=pk)
        serializer = ThankSerializer(teacher,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

        
"""
            ============================
           |        STUDENT VIEW        |
            ============================
"""
class StudentView(APIView):
    def get(self,request,format=None):
        student = Student.objects.filter(active=True)
        serializer = StudentSerializer(student,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class StudentDetailView2(APIView):
    def get(self,request,pk,format=None):
        student = Student.objects.filter(pk=pk).first()
        serializers = StudentSerializer(student)
        return Response(serializers.data,status=status.HTTP_200_OK)
class StudentDetailView(APIView):

    def get_object(self,request):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        student = Student.objects.filter(user_id=payload['id']).first()
        return student
    def get(self,request,format=None):
        student = self.get_object(request)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request,format=None):
        student = self.get_object(request)
        serializer = StudentSerializer(student,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    def delele(self,request,format=None):
        student = self.get_object(request)
        student.delete()
        return Response("success deleted")

class StudentScheduleView(APIView):
    def get(self,request,format=None):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        data = Student.objects.filter(user_id=payload['id']).values('classes_id')
        classId = data[0]['classes_id']
        scheduleDailyList = ScheduleDaily.objects.filter(classes=classId)
        serializer = ScheduleDailySerializer(scheduleDailyList,many=True)
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)

class GetAttendanceStudent(APIView):

    def post(self, request, format=None):
        data = request.data
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        student = Attended.objects.filter(student=payload['id'], datetime=data['date']).first()
        serializer = AttendSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StudentAttendanceView(APIView):
    def get_object(self,request, format=None):
        data = request.data
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        student = Attended.objects.filter(student=payload['id'], datetime=data['date']).first()
        return student


    def post(self, request, format = None):
        data = request.data
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        data['student'] = payload['id']
        serializer = AttendSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def put(self,request,format=None):
        student = self.get_object(request)
        serializer = AttendSerializer1(student, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class StudentAbsentView(APIView):
    def post(self,request,format=None):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        serialzer_data = {
                "student": payload['id'],
                "absent": "true"
            }

        serializer = AttendSerializer(data=serialzer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

class StudentScheduleDetailView(APIView):
    def get_object(self,request,id,format=None):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        data = Student.objects.filter(user_id=payload['id']).values('classes_id')
        classId = data[0]['classes_id']
        scheduleDetail = ScheduleDaily.objects.filter(classes_id=classId,name=id).first()
        return scheduleDetail

    def get(self,request,id,format=None):
        scheduleDetails = self.get_object(request,id)
        taskInstance = Task.objects.filter(scheduleDaily_id=scheduleDetails.id)
        serializer = TaskSerializer(taskInstance,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class StudentTeacherDetailView(APIView):
    def get_object(self,request,format=None):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        data = Student.objects.filter(pk=payload['id']).values('idteacher')
        teacher = data[0]['idteacher']
        teacherdetail = Teacher.objects.filter(user=teacher).first()
        return teacherdetail
    def get(self,request,format=None):
        teacherdetail = self.get_object(request)
        mydata = TeacherSerializer(teacherdetail)
        return Response(data=mydata.data,status=status.HTTP_200_OK)

################################# ACTIVITIES VIEW #################################




class ActivitiesView(APIView):
    #parser_classes = [MultiPartParser,FormParser]
    def get(self,request,format=None):
        serializerdata = GeneralActivities.objects.all()
        serializer = GeneralActivitiesSerializer(serializerdata,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request,format=None):
        serializer = GeneralActivitiesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

class ActivitiesDetailView(APIView):
    def get_object(self,pk,format=None):
        return GeneralActivities.objects.get(pk=pk)

    def get(self,request,pk,format=None):
        actvivites = self.get_object(pk)
        serializers = GeneralActivitiesSerializer(actvivites)
        return Response(serializers.data,status=status.HTTP_200_OK)

    def put(self,request,pk,format=None):
        activities = self.get_object(pk)
        serializer = GeneralActivitiesSerializer(activities,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        activities = self.get_object(pk)
        activities.delete()
        return Response('Xoa thanh cong')

class RegisterActivitiesView(APIView):
    def post(self,request,id,format=None):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        data = {
            "student": payload['id'],
            "activities": id
        }
        serializer = RegisterActivitiesSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class ListRegisterActivitiesView(APIView):
    def get(self, request, format=None):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        activitiesList = ResigterActivities.objects.filter(student=payload['id'])
        serializer = RegisterActivitiesSerializer(activitiesList, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        
############################# Class View ##############################
class ClassDetailView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        classQuery = Student.objects.filter(pk=payload['id']).values('classes')
        classId = classQuery[0]['classes']
        classInstance = Class.objects.filter(pk=classId).first()
        serializer = ClassSerializer(classInstance)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class ClassView(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


######################### Menu View ################################


class MenuView(APIView):

    def get(self,request,format=None):
        menu = Menu.objects.all()
        serializer = MenuSerializer(menu,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = MenuSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)


class MenuDetailView(APIView):

    def get(self, request, pk, format=None):
        meallist = Meal.objects.filter(menu=pk)
        print(meallist)
        serializer = MealSerializer(meallist,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class MenuDetailSessionView(APIView):
    def get(self,request,pk,id,format=None):
        meallist = Meal.objects.filter(menu=pk,sesion=id)
        serializer = MealSerializer(meallist,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,pk,id,format=None):
        data = request.data
        data['sesion']=id
        data['menu']=pk
        serializer = MealSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

class DeleteDetailView(APIView):
    def delete(self, request, pk, format=None):
        meallist = Meal.objects.filter(pk=pk)
        meallist.delete()
        return Response("delete success")

class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer    















