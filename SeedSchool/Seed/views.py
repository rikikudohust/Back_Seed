from calendar import month
from os import stat
import re
from xmlrpc.client import DateTime
from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.decorators import action
from .models import *
from django.http.response import Http404

from rest_framework import serializers, viewsets
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics,status
from rest_framework.parsers import MultiPartParser, FormParser
import jwt
from datetime import date, datetime, timedelta
from django.contrib.auth.models import Group


###################### GROUP ############################
# student_group, created = Group.objects.get_or_create(name='Student')
# admin_group, created = Group.objects.get_or_create(name='Admin')
# teacher_group, created = Group.objects.get_or_create(name='Teacher')

#DECODE
def decode(request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed ('Unauthenicated!')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed ('Unauthenicated!')
        if payload['role'] == 1:
            user = Teacher.objects.filter(pk=payload['id']).first()
            return user
        elif payload['role'] == 2:
            user = Student.objects.filter(pk=payload["id"]).first()
            return user

def bound(month, year):
    set31 = {1,3,5,7,8,10,12}
    set30 = {4,6,9,11}
    set29 = {2}
    date_data = date.today()
    if (month in set31):
        bound1 = date_data.replace(month=month, year=year, day=1)
        bound2 = date_data.replace(month=month, year=year, day=31)
    elif(month in set30):
        bound1 = date_data.replace(month=month, year=year, day=1)
        bound2 = date_data.replace(month=month, year=year, day=30)
    else:
        bound1 = date_data.replace(month=month, year=year, day=1)
        bound2 = date_data.replace(month=month, year=year, day=28)
    data = {
        "bound1": bound1,
        "bound2": bound2
    }
    return data

    

###################### USER VIEW ############################
class RegisterView(APIView):

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            role = serializer.data['role']
            if (role == 2 ):
                user = User.objects.filter(role=role).first()
                #student_group.user_set.add(user)
                student_data = {"user":serializer.data['id'],
                                "email":serializer.data['email'],
                                "name" : request.data['name']
                                }
                student_serializer = StudentSerializer(data=student_data)
                if student_serializer.is_valid():
                    student_serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            elif (role == 1 ):
                user = User.objects.filter(role=role).first()
                #teacher_group.user_set.add(user)
                teacher_data = {"user":serializer.data['id'],
                                "email":serializer.data['email'],
                                "name" : request.data['name']
                                }
                teacher_serializer = TeacherSerializer(data=teacher_data)
                if teacher_serializer.is_valid():
                    teacher_serializer.save()
                    return Response(data=serializer.data,status=status.HTTP_201_CREATED)
            elif (role ==3 ):
                user = User.objects.filter(role=role).first()
                #admin_group.user_set.add(user)
                admin_data = {"user": serializer.data['id'],
                                "email": serializer.data['email'],
                                "name" : request.data['name']
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
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow()
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

class TeacherDetailView2(APIView):
    def get(self,request,pk,format=None):
        teacher = Teacher.objects.filter(pk=pk).first()
        serializers = TeacherSerializer(teacher)
        return Response(serializers.data,status=status.HTTP_200_OK)


class TeacherDetailView(APIView):
    def get_object(self,request):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        teacher = Teacher.objects.filter(user_id=payload['id']).first()
        return teacher

    def get(self,request,format=None):
        teacher = self.get_object(request)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request,format=None):
        teacher = self.get_object(request)
        serializer = TeacherSerializer(teacher,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self,request,format=None):
        teacher = self.get_object(request)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TeacherScheduleView(APIView):
    def get_object(self, request):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        classInstance = Class.objects.filter(teacher=payload['id']).first()
        return classInstance

    def get(self, request, format=None):
        cls = self.get_object(request)
        taskes = Task.objects.filter(classes = cls.id)
        serializer = TaskSerializer(taskes, many = True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        cls = self.get_object(request)
        classId = cls.id
        data = request.data
        data['classes'] = classId
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Need Authorization 
class DeleteOrUpdateSchedule(APIView):
    def get_cls(self, request):
        teacher = decode(request)
        cls = Class.objects.filter(teacher=teacher.pk).first()
        return cls
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404
    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TeacherClassView(APIView):
    def get_object(self, request):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        classInstance = Class.objects.filter(teacher=payload['id']).first()
        return classInstance

    def get(self, request, format=None):
        classInstance = self.get_object(request)
        if classInstance:
            classInstance = self.get_object(request)
            serializer = ClassSerializer(classInstance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'message':'Not Found'},status=status.HTTP_404_NOT_FOUND)


class TeacherStudentView(APIView):
    def get_object(self, request):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        studentListInstance = Student.objects.filter(idteacher=payload['id'])
        return studentListInstance
    
    def get(self, request, format=None):
        studentListInstance = self.get_object(request)
        serializer = StudentSerializer(studentListInstance, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        data = request.data
        classInstance = Class.objects.filter(teacher=payload['id']).first()
        if classInstance == None:
            return Response(data={"message": "Class not found"},status=status.HTTP_404_NOT_FOUND)
        studentInstance = User.objects.filter(email=data['email']).first()
        student = Student.objects.filter(pk = studentInstance.pk).first()
        if student == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(studentInstance)
        data = serializer.data
        data['classes'] = classInstance.id
        data['idteacher'] = payload['id']
        data['avatar'] = None
        serializer_student = StudentSerializer(student, data=data)
        if serializer_student.is_valid():
            serializer_student.save()

            #Increment amount of student in class
            serializer_class = ClassSerializer(classInstance)
            data_class = serializer_class.data
            data_class['amount'] += 1
            serializer_classes = ClassSerializer(classInstance, data=data_class)
            serializer_classes.is_valid(raise_exception=True)
            serializer_classes.save()
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
        print(token)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        student = Student.objects.filter(user_id=payload['id']).first()
        return student
    def get(self,request,format=None):
        student = self.get_object(request)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,format=None):
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
        taskes = Task.objects.filter(classes = classId)
        serializer = TaskSerializer(taskes, many = True)
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)

class GetAttendanceStudent(APIView):

    def get(self, request, format=None):
        data = request.data
        date = request.GET.get('date')
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        student = Attended.objects.filter(student=payload['id'], datetime=date).first()
        serializer = AttendSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StudentAttendanceView(APIView):
    def get_object(self,request,pk, format=None):
        data = request.data
        student = Attended.objects.filter(student=pk, datetime=data['date']).first()
        return student


    def get(self, request,pk, format=None):
        data = request.data
        date = request.GET.get('date')
        student = Attended.objects.filter(student=pk, datetime=date).first()
        if student.absent:
            return Response(data={"message":"absent"}, status=status.HTTP_200_OK)
        serializer = AttendSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request,pk, format = None):
        data = request.data
        data['student'] = pk
        serializer = AttendSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def put(self,request,pk,format=None):
        data = request.data
        date = request.GET.get('date')
        student = Attended.objects.filter(student=pk, datetime=date).first()

        now = datetime.now()
        data = {
            "leave": now,
            "comment": request.data["comment"]
        }
        bound1 = now.replace(minute=30, hour=17, second=0)
        bound2 = now.replace(minute=30, hour=18, second=0)
        
        if now >= bound1 and now < bound2:
            data["surcharge"] = 1
        elif now >= bound2:
            data["surcharge"] = 2
        serializer = AttendSerializer1(student, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class StudentAbsentView(APIView):
    def post(self,request,format=None):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        serializer_data = {
                "student": payload['id'],
                "absent": "true",
            }
        now = datetime.now()
        time = now.replace(minute=0, hour=8, second=0)
        if time > now:
            serializer_data["absent_before"] = True
        serializer = AttendSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

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

class UserNewsView(APIView):
    def get(self,request):
        user = decode(request)
        listNews = PersonalNews.objects.filter(receiver=user.pk)
        serializer = PersonalNewsSerializer(listNews, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ClassNewsView(APIView):
   def get(self,request):
        user = decode(request)
        listNews = ClassNews.objects.filter(receiver=user.classes)
        serializer = PersonalNewsSerializer(listNews, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK) 

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

class ListRegistrationView(APIView):
    def get(self, request, pk, format=None):
        listRegistration = RegisterActivities.objects.filter(activities=pk)
        serializer = RegisterActivitiesSerializer(listRegistration, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ListRegisterActivitiesView(APIView):
    def get(self, request, format=None):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        activitiesList = RegisterActivities.objects.filter(student=payload['id'])
        serializer = RegisterActivitiesSerializer(activitiesList, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        

"""
            ============================
           |         ADMIN VIEW         |
            ============================
"""
############################# Class View ##############################
class ListOrCreateClassView(APIView):
    def get(self, request, format=None):
        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ClassSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class GetOrDeleteOrUpdateClassView(APIView):
    def get_object(self, pk):
        try:
            return Class.objects.get(pk=pk)
        except Class.DoesNotExist:
            raise Http404

    def get(self,request,pk,  format=None):
        classInstance = self.get_object(pk)
        serializer = ClassSerializer(classInstance)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self,request, pk):
        cls = self.get_object(pk)
        cls.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk, format=None):
        cls = self.get_object(pk)
        serializer = ClassSerializer(cls, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


###################### News #####################

class CreateOrListUserNews(APIView):

    def get(self, format=None):
        listNews = News.objects.all()
        serializer = NewsSerializer(listNews, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data
        serializer = NewsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if serializer.data["types"] == 0:
            data1 = {
                "news": serializer.data["id"],
                "receiver": data["receiver"]
            }
            serializer1 = PersonalNewsSerializer(data=data1)
            serializer1.is_valid(raise_exception=True)
            serializer1.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        elif data["types"] == 1:
            data1 = {
                "news": serializer.data["id"],
                "receiver": data["receiver"]
            }
            serializer1 = ClassNewsSerializer(data=data1)
            serializer1.is_valid(raise_exception=True)
            serializer1.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            data1 = {
                "news": serializer.data["id"]
            }
            serializer1 = GeneralNewsSerializer(data=data1)
            serializer1.is_valid(raise_exception=True)
            serializer1.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)


class DeleteOrGetNews(APIView):
    def get(self,request, pk, format=None):
        news = News.objects.get(pk=pk)
        serializer = NewsSerializer(news)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        news = News.objects.get(pk=pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListGeneralNews(APIView):
    def get(self, request, format=None):
        listNews = GeneralNews.objects.all()
        serializer = GeneralNewsSerializer(listNews, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


##################### FEE ################
class CreateOrListFee(APIView):
    def get(self, request, format=None):
        listFee = BasicFee.objects.all()
        serializer = BasicFeeSerializer(listFee, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data= request.data
        serializer = BasicFeeSerializer(data=data)
  
        serializer.is_valid(raise_exception=True)
        serializer.save()
        sesionFee = serializer.data["id"]
        students = Student.objects.all()
        for student in students:
            tuition = data["basicTuition"]
            meal = data["basicMeal"]
            data_date = bound(serializer.data["month"], serializer.data["year"])
            if serializer.data["month"] == 1:
                data_date_before = bound(12, serializer.data["year"]-1)
            else:
                data_date_before = bound(serializer.data["month"] - 1, serializer.data["year"])
            absent_before_8h = Attended.objects.filter(datetime__gte=data_date_before["bound1"],
                                                    datetime__lte=data_date_before["bound2"],
                                                    absent_before=True,
                                                    student=student.pk)
            surcharge1 = Attended.objects.filter(
                                            datetime__gte=data_date["bound1"],
                                            datetime__lte=data_date["bound2"],
                                            absent = False,
                                            surcharge = 1,
                                            student=student.pk
                                        )
            surcharge2 = Attended.objects.filter(
                                            datetime__gte=data_date["bound1"],
                                            datetime__lte=data_date["bound2"],
                                            absent = False,
                                            surcharge = 2,
                                            student=student.pk
                                        )
            reduce = len(absent_before_8h)*serializer.data["basicRedution"]
            surcharge = len(surcharge1)*serializer.data["basicSurcharge1"] + len(surcharge2)*serializer.data["basicSurcharge2"]
            data_store = {
                "student": student.pk,
                "tuition": tuition,
                "meal": meal,
                "surcharge": surcharge,
                "reduce": reduce,
                "sesionFee": sesionFee,
                "debt": tuition + meal + surcharge - reduce
            }
            serializer_fee = FeeSerializer(data=data_store)
            serializer_fee.is_valid(raise_exception=True)
            serializer_fee.save()

        return Response(serializer.data,status=status.HTTP_200_OK)


class GetFee(APIView):
    def get(self, request, format=None):
        student = decode(request)
        monthraw = request.GET.get('month')
        yearraw = request.GET.get('year')
        month = int(monthraw)
        year = int(yearraw)
        sesionFee = BasicFee.objects.filter(month=month, year=year).first()
        if sesionFee == None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        fee = Fee.objects.filter(sesionFee=sesionFee.id, student=student.pk).first()
        serializer = FeeSerializer(fee)
        return Response(data=serializer.data,status=status.HTTP_200_OK)















