from django.shortcuts import render
from rest_framework import generics, serializers,permissions
from rest_framework.response import Response
from service.models import Service
from .serializers import CartItemSerializer
from .models import CartItem
# Create your views here.


class CartItemListView(generics.ListAPIView):
    """
    View to list or create a cart for the current user.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # ✅ Filters cart items belonging only to the authenticated user
        return CartItem.objects.filter(user=self.request.user)

    



class AddServiceToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user = request.user
        service_id = request.data.get('service')
        quantity = int(request.data.get('quantity', 1))

        if not service_id:
            return Response({"error": "Service ID is required"}, status=400)

        service = Service.objects.filter(id=service_id).first()
        if not service:
            return Response({"error": "Invalid service ID"}, status=404)

        #cart, _ = Cart.objects.get_or_create(user=user)

        cart_item, created = CartItem.objects.get_or_create( service=service)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=201)
    
class CartUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to update or delete a cart item.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = []

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()