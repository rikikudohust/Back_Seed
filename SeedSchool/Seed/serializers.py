from django.db import models
from rest_framework import serializers
from .models import (Menu, User,Student,ScheduleDaily,Teacher,Class,GeneralActivities,ResigterActivities,
                    Attended, Task,Admin,Meal,Thank
                     )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ['created_at','updated_at','active',]


class ScheduleDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleDaily
        exclude = ['created_at','updated_at']
    
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        exclude = ['created_at', 'updated_at', 'active']

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class GeneralActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralActivities
        fields = '__all__'

class RegisterActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResigterActivities
        fields = '__all__'

class AttendSerializer(serializers.ModelSerializer):
    class Meta :
        model = Attended
        fields = '__all__'
class AttendSerializer1(serializers.ModelSerializer):
    class Meta :
        model = Attended
        fields = ['comment']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        exclude = ['created_at', 'updated_at',]
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        exclude = ['created_at', 'updated_at', 'active']

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'

class ThankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thank
        fields = '__all__'


