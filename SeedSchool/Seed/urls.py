from django.urls import path,include
from .views import (LoginView,LogoutView,UserView,StudentView,StudentScheduleView,StudentScheduleDetailView,StudentTeacherDetailView,TeacherView,ActivitiesView,RegisterActivitiesView
,ClassDetailView,RegisterView,StudentAbsentView, StudentAttendanceView)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('students',StudentView)
router.register('teachers',TeacherView)
#router.register('classes',ClassView)
router.register('activities',ActivitiesView)
urlpatterns = [

    path('register/', RegisterView.as_view()),
    path('',include(router.urls)),
    path('login/',LoginView.as_view()),
    path('user/',UserView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('students/<int:pk>/schedule',StudentScheduleView.as_view()),
    path('students/<int:pk>/schedule/<int:id>',StudentScheduleDetailView.as_view()),
    path('students/<int:pk>/teacher',StudentTeacherDetailView.as_view()),
    path('class/<int:pk>',ClassDetailView.as_view()),
    path('students/<int:pk>/activities/<int:id>',RegisterActivitiesView.as_view()),
    path('students/<int:pk>/absent',StudentAbsentView.as_view()),
    path('student/<int:pk>/attendance',StudentAttendanceView.as_view()),
    path('teachers/<int:pk>/class', TeacherClassView.as_view()),
    path('teachers/<int:pk>/students', TeacherStudentView.as_view()),
    path('teachers/<int:pk>/schedules', TeacherScheduleView.as_view()),
    path('teachers/<int:pk>/scheduleDaily/<int:id>', TeacherSchdeduleDailyView.as_view()),

]