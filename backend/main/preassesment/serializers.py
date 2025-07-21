
from rest_framework import serializers
import requests
from account.models import User
from account.serializers import UserSerializer
from .models import PreAssesment

class PreAssesmentSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    captcha_token = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = PreAssesment
        fields = '__all__'  # Include all fields
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_captcha_token(self, token):
        secret_key = "6Le4YX8rAAAAAPhg0WybtdtefDhyeX_Vc_Ox9_FL"  # Add this in your settings.py
        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": secret_key, "response": token}
        )
        result = response.json()
        if not result.get("success"):
            raise serializers.ValidationError("Invalid reCAPTCHA. Please try again.")
        return token
    
    # def create(self, validated_data):
    #     user_data = validated_data.pop("user")

    #     # Optional: prevent duplicates
    #     user, _ = User.objects.get_or_create(email=user_data["email"], defaults=user_data)

    #     return PreAssesment.objects.create(user=user, **validated_data)
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        validated_data.pop("captcha_token", None)  # Remove token, it's already validated

        user, created = User.objects.get_or_create(
            email=user_data["email"],
            defaults=user_data
        )

        if not created:
            # Prevent duplicates with phone as well
            if User.objects.filter(phone=user_data.get("phone")).exclude(email=user.email).exists():
                raise serializers.ValidationError({
                    "user": {"phone": ["User with this phone already exists."]}
                })

        return PreAssesment.objects.create(user=user, **validated_data)