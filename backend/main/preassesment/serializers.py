
from rest_framework import serializers

from account.models import User
from account.serializers import UserSerializer
from .models import PreAssesment

class PreAssesmentSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    class Meta:
        model = PreAssesment
        fields = '__all__'  # Include all fields
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        user_data = validated_data.pop("user")

        # Optional: prevent duplicates
        user, _ = User.objects.get_or_create(email=user_data["email"], defaults=user_data)

        return PreAssesment.objects.create(user=user, **validated_data)