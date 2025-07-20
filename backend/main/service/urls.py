from django.urls import path
from . import views

urlpatterns = [
    path('serviceType/', views.ServiceTypeListCreateView.as_view(), name='service-types'),
    path('', views.ServiceListCreateView.as_view(), name='service-list'),
    path('<int:pk>/', views.ServiceDetailView.as_view(), name='service-detail'),
    path('<int:pk>/update/', views.ServiceUpdateDeleteView.as_view(), name='service-update'),
    path('<int:pk>/delete/', views.ServiceUpdateDeleteView.as_view(), name='service-delete'),
]