from rest_framework import serializers
from .models import Teacher, User,Student,ScheduleDaily, Class, Schedule, Attended
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','password','role']
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
        fields = '__all__'
    
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        exclude = ['created_at','updated_at']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        exclude = ['created_at', 'updated_at', 'active']

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
    
class AttendSerializer(serializers.ModelSerializer):
    class Meta :
        model = Attended
        fields = '__all__'