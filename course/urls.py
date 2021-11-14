from django.urls import path
from . import views

urlpatterns = [
    path('course_create/', views.course_create, name='course_create'),
    path('course_update/', views.course_update, name='course_update'),
    path('course_delete/', views.course_delete, name='course_delete'),
    path('course_list/', views.course_list, name='course_list'),
]