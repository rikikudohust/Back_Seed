from django.contrib import admin
from .models import User,Teacher,Student,ScheduleDaily,GeneralActivities,Class,ResigterActivities,Attended,Task,Menu,Meal

# Register your models here.
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(GeneralActivities)
admin.site.register(ScheduleDaily)
admin.site.register(Class)
admin.site.register(ResigterActivities)
admin.site.register(Attended)
admin.site.register(Task)
admin.site.register(Meal)
admin.site.register(Menu)

