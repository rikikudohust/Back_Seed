from django.contrib import admin
from .models import User,Teacher,Student,Schedule,ScheduleDaily,GeneralActivities
# Register your models here.
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Schedule)
admin.site.register(ScheduleDaily)
