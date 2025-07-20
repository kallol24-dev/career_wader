
from account.serializers import UserSerializer
from rest_framework import serializers
from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"

# class CartSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True, read_only=True)
#     user = UserSerializer(read_only=True)

#     class Meta:
#         model = Cart
#         fields = "__all__"