from django.urls import path

from . import views

urlpatterns = [
    path('', views.BlogCreateListView.as_view()),
    path('<int:pk>/', views.BlogRetrieveUpdateDeleteView.as_view()),
]