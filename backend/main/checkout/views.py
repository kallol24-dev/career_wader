from django.shortcuts import render

# Create checout form CheckoutForm

from rest_framework import generics, filters, permissions
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
    queryset = Checkout.objects.all().order_by('-created_at')
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['city', 'state', 'name', 'email', 'phone', 'service__name', 'status']
    filterset_fields = ['state']

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            #print("Authenticated user:", user.id)
            franchise = user.franchise  # or user.franchise_set.first() if reverse FK
            instance = serializer.save(franchaise_uuid=franchise)
        else:
            instance = serializer.save()
        print("Checkout created for:", instance.name)
        
        # if user.is_authenticated:
        #     try:
        #         franchise = user.franchise  # assuming OneToOneField or ForeignKey
        #         instance = serializer.save(franchaise_uuid=franchise)
        #     except AttributeError:
        #         # fallback if franchise not set
        #         #instance = serializer.save()
        #     else:
        # # Do not pass franchaise_uuid
        #         instance = serializer.save()
            

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated :
            if user.is_staff or user.is_superuser:
                print("Admin access granted")
                return Checkout.objects.all().order_by('-created_at')
            print(user.franchise.franchaise_uuid)
            return Checkout.objects.filter(franchaise_uuid=user.franchise.franchaise_uuid).order_by('-created_at')
        return Checkout.objects.none()  # ✅ No user filter needed  # or all() if public
        
    