from rest_framework import serializers
from .models import ServiceType, Service


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['id', 'name', 'created_at', 'updated_at']


class ServiceSerializer(serializers.ModelSerializer):
    type_name = serializers.ReadOnlyField(source='type.name')

    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'base_price',
            'sale_price',
            'type',         # foreign key (ID)
            'type_name',    # human-readable name
            'description',
            'available',
            'created_at',
            'updated_at',
        ]
