from django.urls import path
from .views import *
urlpatterns = [
    path('main/', main, name="main"),
    path('test/', test, name="test"),
    path('set_place_detail/', set_place_detail, name="set_place_detail"),
    path('<str:kakao_place_id>/', get_place_detail, name="get_place_detail"),
]
