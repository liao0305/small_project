# coding:utf-8
# Data:2019/3/7
from django.conf.urls import url, include
from . import views

urlpatterns = [
    # url(r'^templist/', views.GetTempList.as_view()),
    url(r'^templist/', views.get_templist),
    url(r'^tempdetail/', views.get_temp_deatil),
    url(r'^generate/', views.generate_photo),
    url(r'^(\w+).jpg', views.show_photo),
    url(r'(\S+)', views.show_create_photo),
]
