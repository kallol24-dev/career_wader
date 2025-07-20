from django.shortcuts import render

# Create checout form CheckoutForm

from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import checkoutSerializer
from .models import Checkout
from django_filters.rest_framework import DjangoFilterBackend

class CheckoutCreateListView(generics.ListCreateAPIView):
    """
    View to create a checkout for the current user.
    """
    serializer_class = checkoutSerializer
    permission_classes = []
    queryset = Checkout.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status'] 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Checkout.objects.filter(user=self.request.user)
        return Checkout.objects.none()  # or all() if public
        
    