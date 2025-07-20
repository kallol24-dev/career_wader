from django.urls import path
from . import views
urlpatterns = [
    path('', views.CheckoutCreateListView.as_view(), name='checkout-create-list'),
    
]