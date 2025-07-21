from rest_framework import serializers
from . import views
from django.urls import path

urlpatterns = [
    
path("register/", views.StudentRegisterView.as_view(), name="student-register"),
path("", views.StudentListView.as_view(), name="students-list"),
]
