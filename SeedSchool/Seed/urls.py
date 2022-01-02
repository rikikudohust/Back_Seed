from django.urls import path,include
from .views import (LoginView,LogoutView, StudentView#UserView
                    , StudentScheduleView, StudentScheduleDetailView
                    , StudentTeacherDetailView, TaskView, TeacherView
                    , ClassDetailView
                    , RegisterView, StudentAbsentView, StudentAttendanceView
                    , TeacherClassView, TeacherStudentView,StudentDetailView2
                    , TeacherScheduleView, TeacherScheduleDetailView,GetAttendanceStudent
                    , RegisterActivitiesView, ListRegisterActivitiesView,TeacherThankView,ActivitiesView,ActivitiesDetailView
                    , ClassView,MenuView,MenuDetailView,MenuDetailSessionView,DeleteDetailView,StudentDetailView,TeacherDetailView )
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('classes',ClassView)
router.register('taskes',TaskView)
urlpatterns = [

    path('register/', RegisterView.as_view()),
    path('',include(router.urls)),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
   # path('users/',UserView.as_view()),

    path('students/',StudentView.as_view()),
    path('students/profile',StudentDetailView.as_view()),
    path('students/<int:pk>', StudentDetailView2.as_view()),
    path('students/schedules',StudentScheduleView.as_view()),
    path('students/schedules/<int:id>',StudentScheduleDetailView.as_view()),
    path('students/teachers',StudentTeacherDetailView.as_view()),
    path('students/activities', ListRegisterActivitiesView.as_view()),
    path('students/activities/<int:id>',RegisterActivitiesView.as_view()),
    path('students/absent',StudentAbsentView.as_view()),
    path('students/attendance',StudentAttendanceView.as_view()),
    path('students/attend', GetAttendanceStudent.as_view()),
    path('students/class', ClassDetailView.as_view()),

    path('teachers/',TeacherView.as_view()),
    path('teachers/<int:pk>/update',TeacherDetailView.as_view()),
    path('teachers/<int:pk>/class', TeacherClassView.as_view()),
    path('teachers/<int:pk>/students', TeacherStudentView.as_view()),
    path('teachers/<int:pk>/schedules', TeacherScheduleView.as_view()),
    path('teachers/<int:pk>/schedules/<int:id>', TeacherScheduleDetailView.as_view()),
    path('teachers/<int:pk>/thank',TeacherThankView.as_view()),



    path('menus',MenuView.as_view()),
    path('menus/<int:pk>/sesion',MenuDetailView.as_view()),
    path('menus/<int:pk>/sesion/<int:id>',MenuDetailSessionView.as_view()),
    path('meal/<int:pk>', DeleteDetailView.as_view()),

    path('activities/',ActivitiesView.as_view()),
    path('activities/<int:pk>/',ActivitiesDetailView.as_view()),


]