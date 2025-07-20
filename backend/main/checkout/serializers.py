

from checkout.models import Checkout
from rest_framework import serializers

class checkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = "__all__"