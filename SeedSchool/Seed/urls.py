from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#router.register('users',views.UserViewSet)
#router.register('teachers',views.TeachearViewSet)
#router.register('schedules',views.ScheduleViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('login/',views.UserView.as_view),
]
