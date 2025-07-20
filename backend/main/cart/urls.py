from django.urls import path
from . import views
urlpatterns = [
    # path('', views.CartListCreateView.as_view(), name='cart-list-create'),
    path('', views.CartItemListView.as_view(), name='cart-item-list'),
    path('add-service/', views.AddServiceToCartView.as_view(), name='add-service-to-cart'),
    path('<int:pk>/update/', views.CartUpdateDeleteView.as_view(), name='cart-item-update'),
    path('<int:pk>/delete/', views.CartUpdateDeleteView.as_view(), name='cart-item-delete'),
]