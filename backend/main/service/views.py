from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import ServiceType, Service
from .serializers import ServiceTypeSerializer, ServiceSerializer


# List and Create Service Types (optional to expose this to admin only)
class ServiceTypeListCreateView(generics.ListCreateAPIView):
    queryset = ServiceType.objects.all().order_by('name')
    serializer_class = ServiceTypeSerializer
    permission_classes = []


# List all services or create a new service
    
class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all().order_by('name')
    serializer_class = ServiceSerializer
    permission_classes = []
    filterset_fields = ['type__name', 'available']


# Retrieve a single service by ID
class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = []

class ServiceUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = []
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
    
    def perform_destroy(self, instance):
        instance.delete()