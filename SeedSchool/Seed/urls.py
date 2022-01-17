from ast import Del
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('taskes',TaskView)
urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
   # path('users/',UserView.as_view()),

    path('students/',StudentView.as_view()),
    path('students/profile',StudentDetailView.as_view()),
    path('students/<int:pk>', StudentDetailView2.as_view()),
    path('students/schedules',StudentScheduleView.as_view()),
    path('students/teachers',StudentTeacherDetailView.as_view()),
    path('students/activities', ListRegisterActivitiesView.as_view()),
    path('students/activities/<int:id>',RegisterActivitiesView.as_view()),
    path('students/absent',StudentAbsentView.as_view()),
    path('students/<int:pk>/attendance',StudentAttendanceView.as_view()),
    path('students/attend', GetAttendanceStudent.as_view()),
    path('students/person_news', UserNewsView.as_view()),
    path('students/class_news', ClassNewsView.as_view()),
    path('students/fee', GetFee.as_view()),
    # path('students/class', ClassDetailView.as_view()),

    path('teachers/',TeacherView.as_view()),
    path('teachers/profile',TeacherDetailView.as_view()),
    path('teachers/students', TeacherStudentView.as_view()),
    path('teachers/schedules', TeacherScheduleView.as_view()),
    path('teachers/schedules/<int:pk>', DeleteOrUpdateSchedule.as_view()),
    path('teachers/<int:pk>/thank',TeacherThankView.as_view()),
    path('teachers/person_news', UserNewsView.as_view()),

    path('classes/', ListOrCreateClassView.as_view()),
    path('classes/<int:pk>/',GetOrDeleteOrUpdateClassView.as_view()),

    path('menus',MenuView.as_view()),
    path('menus/<int:pk>/sesion',MenuDetailView.as_view()),
    path('menus/<int:pk>/sesion/<int:id>',MenuDetailSessionView.as_view()),
    path('meal/<int:pk>', DeleteDetailView.as_view()),


    path('activities/',ActivitiesView.as_view()),
    path('activities/<int:pk>/',ActivitiesDetailView.as_view()),
    path('activities/<int:pk>/amount', ListRegistrationView.as_view()),

    path('news/', CreateOrListUserNews.as_view()),
    path('news/<int:pk>', DeleteOrGetNews.as_view()),
    path('news/general', ListGeneralNews.as_view()),

    path('fee/', CreateOrListFee.as_view()),
]