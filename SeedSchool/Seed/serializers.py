from django.db import models
from rest_framework import serializers
from .models import *
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
        model = RegisterActivities
        fields = '__all__'

class AttendSerializer(serializers.ModelSerializer):
    class Meta :
        model = Attended
        fields = '__all__'
class AttendSerializer1(serializers.ModelSerializer):
    class Meta :
        model = Attended
        fields = ['comment','surcharge','leave']

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

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"
  
class PersonalNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalNews
        fields = "__all__"

class ClassNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassNews
        fields = "__all__"
  
class GeneralNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralNews
        fields = "__all__"

class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = '__all__'

class BasicFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicFee
        fields = '__all__'
  

