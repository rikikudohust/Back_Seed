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

    path('students/',StudentView.as_view()), #lay thong tin cua tat ca hoc sinh
    path('students/<int:pk>/profile',StudentDetailView.as_view()), #lay thong tin cua 1 hoc sinh
    path('students/<int:pk>/schedules',StudentScheduleView.as_view()), #lay tat ca thoi khoa bieu
    path('students/<int:pk>/teachers',StudentTeacherDetailView.as_view()),
    path('students/<int:pk>/activities', ListRegisterActivitiesView.as_view()),
    path('students/<int:pk>/activities/<int:id>',RegisterActivitiesView.as_view()),
    path('students/<int:pk>/absent',StudentAbsentView.as_view()),
    path('students/<int:pk>/attendance',StudentAttendanceView.as_view()),
    path('students/<int:pk>/attend', GetAttendanceStudent.as_view()),
    path('students/<int:pk>/person_news', UserNewsView.as_view()),
    path('students/<int:pk>/class_news', ClassNewsView.as_view()),
    path('students/<int:pk>/fee', GetFee.as_view()),
    # path('students/class', ClassDetailView.as_view()),

    path('teachers/',TeacherView.as_view()),
    path('teachers/<int:pk>/profile',TeacherDetailView.as_view()),
    path('teachers/<int:pk>/students', TeacherStudentView.as_view()),
    path('teachers/<int:pk>/schedules', TeacherScheduleView.as_view()),
    path('teachers/schedules/<int:pk>', DeleteOrUpdateSchedule.as_view()),
    path('teachers/<int:pk>/thank',TeacherThankView.as_view()),
    path('teachers/<int:pk>/person_news', UserNewsView.as_view()),

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