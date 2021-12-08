from django.urls import path,include
from .views import LoginView,LogoutView, TeacherSchdeduleDetailView, TeacherScheduleView, TeacherView,UserView,StudentView,StudentScheduleView
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
    path('students/<int:pk>/schedule',StudentScheduleView.as_view()),
    path('teachers/<int:pk>/schedule', TeacherScheduleView.as_view()),
    path('teachers/<int:pk>/schedule/<int:id>', TeacherSchdeduleDetailView.as_view())
]