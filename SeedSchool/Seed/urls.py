from django.urls import path,include
from .views import (LoginView,LogoutView, StudentView#UserView
                    , StudentScheduleView, StudentScheduleDetailView
                    , StudentTeacherDetailView, TaskView, TeacherView, ActivitiesView
                    , RegisterActivitiesView, ClassDetailView
                    , RegisterView, StudentAbsentView, StudentAttendanceView
                    , TeacherClassView, TeacherStudentView
                    , TeacherScheduleView, TeacherScheduleDetailView,GetAttendanceStudent
                    , RegisterActivitiesView, ListRegisterActivitiesView,TeacherThankView,UpdateActivitiesView,UpdateDetailView
                    , ClassView,MenuView,MenuDetailView,MenuDetailSessionView,DeleteDetailView,UpdateStudentView,UpdateTeacherView)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('classes',ClassView)
router.register('activities',ActivitiesView)
router.register('taskes',TaskView)
urlpatterns = [

    path('register/', RegisterView.as_view()),
    path('',include(router.urls)),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
   # path('users/',UserView.as_view()),

    path('students/',StudentView.as_view()),
    path('students/<int:pk>/update',UpdateStudentView.as_view()),
    path('students/<int:pk>/schedules',StudentScheduleView.as_view()),
    path('students/<int:pk>/schedules/<int:id>',StudentScheduleDetailView.as_view()),
    path('students/<int:pk>/teachers',StudentTeacherDetailView.as_view()),
    path('students/<int:pk>/activities', ListRegisterActivitiesView.as_view()),
    path('students/<int:pk>/activities/<int:id>',RegisterActivitiesView.as_view()),
    path('students/<int:pk>/absent',StudentAbsentView.as_view()),
    path('students/<int:pk>/attendance',StudentAttendanceView.as_view()),
    path('students/<int:pk>/attend', GetAttendanceStudent.as_view()),
    path('students/<int:pk>/class', ClassDetailView.as_view()),

    path('teachers/',TeacherView.as_view()),
    path('teachers/<int:pk>/update',UpdateTeacherView.as_view()),
    path('teachers/<int:pk>/class', TeacherClassView.as_view()),
    path('teachers/<int:pk>/students', TeacherStudentView.as_view()),
    path('teachers/<int:pk>/schedules', TeacherScheduleView.as_view()),
    path('teachers/<int:pk>/schedules/<int:id>', TeacherScheduleDetailView.as_view()),
    path('teachers/<int:pk>/thank',TeacherThankView.as_view()),



    path('menus',MenuView.as_view()),
    path('menus/<int:pk>/sesion',MenuDetailView.as_view()),
    path('menus/<int:pk>/sesion/<int:id>',MenuDetailSessionView.as_view()),
    path('meal/<int:pk>', DeleteDetailView.as_view()),

    path('activities/post',UpdateActivitiesView.as_view()),
    path('activities/<int:pk>/update',UpdateDetailView.as_view()),


]