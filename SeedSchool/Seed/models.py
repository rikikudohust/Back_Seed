from calendar import month
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.files import ImageField
# Create your models here.


class User(AbstractUser):
    TEACHER = 1
    STUDENT = 2
    ADMIN = 3

    ROLE_CHOICES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
        (ADMIN,'Admin'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)


class MyModelBase(models.Model):

    Sex = [
        (0,'Nam'),
        (1,'Nữ'),
    ]
    name = models.CharField(max_length=255,default='')
    # email = models.CharField(max_length=30,blank=False,unique=True)
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

class Admin(MyModelBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return self.name

class Teacher(MyModelBase):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    phone = models.CharField(max_length=30,default='',null=True,blank=True)
    address = models.CharField(max_length=30,default='',null=True,blank=True)
    position = models.CharField(max_length=30,default='',null=True,blank=True)
    achievement = models.CharField(max_length=4000,default='',null=True,blank=True)
    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=255,unique=True,default='')
    teacher = models.OneToOneField('Teacher',on_delete=models.CASCADE,default='', null=True)
    amount = models.IntegerField(default=0,blank=False)

    def __str__(self):
        return self.name

class Student(MyModelBase):
    user = models.OneToOneField('User', on_delete=models.CASCADE, default='', primary_key=True)
    nameparent = models.CharField(max_length=30,default='',null=True,blank=True)
    phoneparent = models.CharField(max_length=30,default='',null=True,blank=True)
    address = models.CharField(max_length=30,default='',null=True,blank=True)
    idteacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,default='',null=True,blank=True)
    classes = models.ForeignKey('Class',on_delete=models.CASCADE,default='',null=True,blank=True)

class Task(models.Model):
    #Lesson
    # lesson1 = "LESSON1"
    # lesson2 = "LESSON2"
    # lesson3 = "LESSON3"
    # lesson4 = "LESSON4"
    # #DAILY
    # MONDAY = 'Monday'
    # TUESDAY = 'Tuesday'
    # WEDNESDAY = 'Wednesday'
    # THURSDAY = 'Thursday'
    # FRIDAY = 'Friday'
    # SATURDAY = 'Saturday'
    # SUNDAY = 'Sunday'

    # Daily = [
    #     (MONDAY, 'Monday'),
    #     (TUESDAY, 'Tuesday'),
    #     (WEDNESDAY, 'Wednesday'),
    #     (THURSDAY, 'Thursday'),
    #     (FRIDAY, 'Friday'),
    #     (SATURDAY, 'Saturday'),
    #     (SUNDAY, 'Sunday'),
    # ]
    # Lesson = [
    #     (lesson1, "LESSON1"),
    #     (lesson2, "LESSON2"),
    #     (lesson3, "LESSON3"),
    #     (lesson4, "LESSON4"),
    # ]
    # daily = models.CharField(choices=Daily, max_length=255, default=MONDAY)
    # lesson = models.CharField(choices=Lesson, max_length=255, default=lesson1)
    t_11 = models.CharField(max_length=255, default='')
    t_12 = models.CharField(max_length=255, default='')
    t_13 = models.CharField(max_length=255, default='')
    t_14 = models.CharField(max_length=255, default='')
    t_15 = models.CharField(max_length=255, default='')
    t_21 = models.CharField(max_length=255, default='')
    t_22 = models.CharField(max_length=255, default='')
    t_23 = models.CharField(max_length=255, default='')
    t_24 = models.CharField(max_length=255, default='')
    t_25 = models.CharField(max_length=255, default='')
    t_31 = models.CharField(max_length=255, default='')
    t_32 = models.CharField(max_length=255, default='')
    t_33 = models.CharField(max_length=255, default='')
    t_34 = models.CharField(max_length=255, default='')
    t_35 = models.CharField(max_length=255, default='')
    t_41 = models.CharField(max_length=255, default='')
    t_42 = models.CharField(max_length=255, default='')
    t_43 = models.CharField(max_length=255, default='')
    t_44 = models.CharField(max_length=255, default='')
    t_45 = models.CharField(max_length=255, default='')
    classes = models.ForeignKey('Class', on_delete=models.CASCADE, null=True)
    version = models.IntegerField(default=0, null=True)

class GeneralActivities(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    eventdate = models.DateField(default='')
    description = models.CharField(max_length=4000, default='')
    title = models.CharField(max_length=255, default='')
    is_register = models.BooleanField(default=True)
    location = models.CharField(max_length=255, default='')
    image = models.ImageField(upload_to='Seed/activities/%Y/%m', default='', blank=True, null=True)

    def __str__(self):
        return self.description

class RegisterActivities(models.Model):
    student = models.ForeignKey('Student',on_delete=models.CASCADE)
    activities = models.ForeignKey(GeneralActivities,on_delete=models.CASCADE)

class Menu(models.Model):
    Daily = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    name = models.IntegerField(choices=Daily, default='0',primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='Seed/%Y/%m', default='', blank=True, null=True)



class Meal(models.Model):
    Sesion = [
        (0, 'Breakfast'),
        (1, 'Lunch'),
        (2, 'Dinner'),
    ]
    sesion = models.IntegerField(choices=Sesion, default='0')
    menu = models.ForeignKey(Menu,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,blank=False)
    image = models.ImageField(upload_to='Seed/%Y/%m', default='', blank=True, null=True)

class Attended(models.Model):
    student = models.IntegerField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    absent = models.BooleanField(default=False)
    absent_before = models.BooleanField(default=False)
    comment = models.CharField(max_length=255,default='',blank=True, null=True)
    leave = models.DateTimeField(auto_now=True,blank=True, null=True)
    surcharge = models.IntegerField(default=0)
    image = models.ImageField(upload_to='Seed/%Y/%m', default='', blank=True, null=True)
    datetime = models.DateField(auto_now_add=True)

class Thank(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,default='')
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=255, default='')


class News(models.Model):
    PERSONAL = 0
    CLASS = 1
    ALL = 2
    Type = [
        (PERSONAL, 'PERSONAL'),
        (CLASS, 'CLASS'),
        (ALL, 'ALL')
    ]
    title = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='')
    types = models.IntegerField(choices=Type, default=ALL)
    create_at = models.DateTimeField(auto_now_add=True)

class PersonalNews(models.Model):
    receiver =  models.ForeignKey('User',on_delete=models.CASCADE)
    news = models.ForeignKey('News',on_delete=models.CASCADE)

class ClassNews(models.Model):
    receiver =  models.ForeignKey('Class',on_delete=models.CASCADE)
    news = models.ForeignKey('News',on_delete=models.CASCADE)

class GeneralNews(models.Model):
    news = models.ForeignKey('News',on_delete=models.CASCADE)

class Fee(models.Model):
    tuition = models.IntegerField(default=0)
    meal = models.IntegerField(default=0)
    surcharge = models.IntegerField(default=0)
    redution = models.IntegerField(default=0)
    paid = models.IntegerField(default=0)
    debt = models.IntegerField(default=0)
    sesionFee = models.ForeignKey('BasicFee', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

class BasicFee(models.Model):
    month = models.IntegerField(default=1)
    year = models.IntegerField(default=2022)
    basicTuition = models.IntegerField(default=0)
    basicMeal = models.IntegerField(default=0)
    basicSurcharge1 = models.IntegerField(default=0)
    basicSurcharge2 = models.IntegerField(default=0)
    basicRedution = models.IntegerField(default=0)



