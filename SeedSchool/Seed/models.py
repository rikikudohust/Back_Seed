from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.files import ImageField
# Create your models here.


class User(AbstractUser):
    TEACHER = 1
    STUDENT = 2

    ROLE_CHOICES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)


class MyModelBase(models.Model):

    Sex = [
        (0,'Nam'),
        (1,'Nữ'),
    ]
    name = models.CharField(max_length=255,default='')
    email = models.CharField(max_length=30,blank=False,unique=True)
    sex = models.IntegerField(choices=Sex,default=0)
    avatar = models.ImageField(upload_to='Seed/%Y/%m', default='',blank=True,null=True)
    age = models.IntegerField(default=0,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    class Meta:
        abstract = True

class Teacher(MyModelBase):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=255,unique=True,default='')
    teacher = models.OneToOneField('Teacher',on_delete=models.CASCADE,default='')
    amount = models.IntegerField(default=0,blank=False)
    teacher_name = models.CharField(max_length=255,default='')

    def __str__(self):
        return self.name

class Student(MyModelBase):
    user = models.OneToOneField('User', on_delete=models.CASCADE, default='', primary_key=True)
    nameparent = models.CharField(max_length=30,default='',null=True,blank=True)
    phoneparent = models.CharField(max_length=30,default='',null=True,blank=True)
    address = models.CharField(max_length=30,default='',null=True,blank=True)
    idteacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,default='',null=True,blank=True)
    schedule = models.ForeignKey('Schedule',on_delete=models.CASCADE,default='',null=True,blank=True)
    classes = models.ForeignKey('Class',on_delete=models.CASCADE,default='',null=True,blank=True)

class Schedule(models.Model):
    classes = models.OneToOneField('Class', on_delete=models.CASCADE, default='', primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ScheduleDaily(models.Model):
    Daily = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    Time = [
        (0, '0'),
        (1, '1'),
        (2, '2'), (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'), (8, '8'),
        (9, '9'),(10, '10'),
        (7, '7'),(11, '11'),(12, '12'),

    ]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.IntegerField(choices=Daily,default='0')
    time_start = models.IntegerField(choices=Time,default='0')
    time_finish = models.IntegerField(choices=Time, default='0')
    task = models.CharField(max_length=255,blank=False)
    schedule = models.ForeignKey(Schedule,related_name='Schedule',on_delete=models.CASCADE)

class GeneralActivities(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    eventdate = models.DateField(default='')
    description = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.description

class ResigterActivities(models.Model):
    student = models.ForeignKey('Student',on_delete=models.CASCADE)
    activities = models.ForeignKey(GeneralActivities,on_delete=models.CASCADE)

class Menu(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    session = models.CharField(max_length=30,blank=False)

class Meal(models.Model):
    idmenu = models.ForeignKey(Menu,related_name='menu',on_delete=models.CASCADE)
    name = models.CharField(max_length=255,blank=False)

class Attended(models.Model):
    student = models.IntegerField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    absent = models.BooleanField(default=False)
    commment = models.CharField(max_length=255,default='',blank=True, null=True)
    leave = models.DateTimeField(auto_now=True,blank=True, null=True)
    image = models.ImageField(upload_to='Seed/%Y/%m', default='', blank=True, null=True)

class Thank(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,default='')
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    commment = models.CharField(max_length=255, default='')

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,default='')
    totalfee = models.IntegerField(default=0)
    semester = models.CharField(max_length=255,default='',)
    tuition = models.IntegerField(default=0)
    mealfee = models.IntegerField(default=0)
