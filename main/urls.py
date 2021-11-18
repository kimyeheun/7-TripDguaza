from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('userinfo/', views.userinfo, name='userinfo'),
    path('userinfo_update/', views.userinfo_update, name='userinfo_update'),
]
