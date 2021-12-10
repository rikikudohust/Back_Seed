from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Seed import views
urlpatterns = [
    path('menu/', views.MenuList.as_view()),
    path('menu/<int:pk>/', views.MenuDetail.as_view()),
]