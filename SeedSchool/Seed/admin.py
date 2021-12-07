from django.contrib import admin
from .models import User,Teacher,Student,Schedule,ScheduleDaily,GeneralActivities,Class
# Register your models here.
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(GeneralActivities)
admin.site.register(Schedule)
admin.site.register(ScheduleDaily)
admin.site.register(Class)
