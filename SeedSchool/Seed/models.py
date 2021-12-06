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

