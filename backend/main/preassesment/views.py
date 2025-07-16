from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from account.models import User
from account.serializers import UserSerializer
from .models import PreAssesment
from .serializers import PreAssesmentSerializer

class PreAssesmentListCreateView(generics.ListCreateAPIView):
    serializer_class = PreAssesmentSerializer
    permission_classes = []

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return PreAssesment.objects.all()
        return PreAssesment.objects.none()  # prevent students from seeing others’ data
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['require_password'] = False  # or True if this is a registration view
        return context
    
    def perform_create(self, serializer):
        user_data = self.request.data.get("user")
        if not user_data:
            raise ValidationError({"user": "User data is required."})

        email = user_data.get("email")
        if not email:
            raise ValidationError({"user.email": "Email is required."})

        # Prevent duplicate submissions
        if PreAssesment.objects.filter(user__email=email).exists():
            raise ValidationError("This user has already submitted a pre-assessment.")

        serializer.save()

    # def perform_create(self, serializer):
    #     user = self.request.user
    #     if user.is_staff:
    #         raise ValidationError("Admins cannot create pre-assessments.")
    #     if PreAssesment.objects.filter(user=user).exists():
    #         raise ValidationError("You have already submitted a pre-assessment.")
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user=user)
    # def create(self, validated_data):
    #     user_data =  self.request.data.pop("user")
    #     # Check for existing user (optional)
    #     if User.objects.filter(email=user_data['email']).exists():
    #         raise ValidationError({"user": "A user with this email already exists."})

    #     user_serializer = UserSerializer(data=user_data, context={'require_password': False})
    #     user_serializer.is_valid(raise_exception=True)
    #     user = user_serializer.save()

    #     data["user"] = user.id  # Only if using PrimaryKeyRelatedField in serializer

    # serializer = self.get_serializer(data=data)
    # serializer.is_valid(raise_exception=True)

    # self.perform_create(serializer)
    # return Response(serializer.data, status=201)    