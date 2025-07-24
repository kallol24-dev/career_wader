from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationsListView.as_view(), name='notification-list'),
]
