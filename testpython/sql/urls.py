from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('notice/', views.notice, name='notice'),
    path('noticeAdd/', views.noticeAdd, name='noticeAdd'),
    path('notice/<int:pk>/', views.posting, name="posting"),

]

