from django.db import models
from django.contrib.auth.models import AbstractUser
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
    avatar = models.ImageField(upload_to='Seed/%Y/%m', default='')
    age = models.IntegerField(default=0,blank=False)
    Class = models.CharField(max_length=30,blank=False,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    class Meta:
        abstract = True

class Teacher(MyModelBase):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    schedule = models.OneToOneField('Schedule',on_delete=models.CASCADE,default='')

class Student(MyModelBase):
    user = models.OneToOneField('User', on_delete=models.CASCADE, default='', primary_key=True)
    nameparent = models.CharField(max_length=30,default='')
    phoneparent = models.CharField(max_length=30,default='')
    address = models.CharField(max_length=30,default='')
    idteacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    idshedule = models.ForeignKey('Schedule',on_delete=models.CASCADE)
    activities = models.ManyToManyField('GeneralActivities',blank=True,related_name='activities')

class Schedule(models.Model):
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
    schedule= models.ForeignKey(Schedule, on_delete=models.CASCADE)



class GeneralActivities(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    eventdate = models.DateField(default='')
    description = models.CharField(max_length=255, default='')



