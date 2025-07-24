

from checkout.models import Checkout
from service.models import Service
from service.serializers import ServiceSerializer
from rest_framework import serializers

# from franchaise.serializers import FranchiseSerializer

class checkoutSerializer(serializers.ModelSerializer):
    # service = ServiceSerializer(many=True, read_only=True, source='checkouts')
    # franchise = FranchiseSerializer(many=True, read_only=True, source='checkouts' )
    service = ServiceSerializer(read_only=True)  # 👈 for output (GET)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='service',  # 👈 map to FK field
        write_only=True
    )
    class Meta:
        model = Checkout
        fields = [
            'id', 'name', 'email', 'phone',
            'address', 'city', 'state', 'status', 'service',
            'service_id', 'franchaise_uuid_id' , 'created_at', 'updated_at'
        ]
        read_only_fields = ['franchaise_uuid']
