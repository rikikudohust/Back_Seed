from django.urls import path,include
from .views import LoginView,LogoutView, TeacherSchdeduleDailyView, TeacherScheduleView, TeacherStudentView, TeacherView,UserView,StudentView,StudentScheduleView, TeacherClassView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('students',StudentView)
router.register('teachers', TeacherView)
urlpatterns = [

    #path('register/', RegisterView.as_view()),
    path('',include(router.urls)),
    path('login/',LoginView.as_view()),
    path('user/',UserView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('students/<int:pk>/schedules',StudentScheduleView.as_view()),
    path('teachers/<int:pk>/class', TeacherClassView.as_view()),
    path('teachers/<int:pk>/students', TeacherStudentView.as_view()),
    # path('teachers/<int:pk>/schedules', TeacherScheduleView.as_view()),
    # path('teachers/<int:pk>/scheduleDaily/<int:id>', TeacherSchdeduleDailyView.as_view()),
    # path('teachers/<int:pk>/classes', TeacherClassView.as_view()),
]