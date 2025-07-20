from rest_framework import serializers
from .models import PlacementEnquiry


class PlacementEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacementEnquiry
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']