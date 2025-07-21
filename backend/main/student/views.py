from django.shortcuts import render

from franchaise.models import Franchise
from .filters import FilterClassStudent
from rest_framework import generics, filters,permissions
from django.db import transaction
from datetime import timedelta
import random
from django.utils import timezone
from rest_framework.exceptions import APIException
from account.views import EmailSendFailed, send_zeptomail
from .models import Student
from main.pagination import CustomPageNumberPagination
from .serializers import StudentSerializer
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

class StudentRegisterView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = []  # Allow public registration
    
    @transaction.atomic
    def perform_create(self, serializer):
        student = serializer.save()
        user = student.user
        print(student.user.first_name)
        
        
        
        
        # Generate 6-digit code
        verification_code = str(random.randint(100000, 999999))

        # Set expiry time to 10 minutes from now
        expiry_time = timezone.now() + timedelta(minutes=10)

        # Save to user
        user.verification_code = verification_code
        user.verification_expiry = expiry_time
        user.save(update_fields=['verification_code', 'verification_expiry'])
        

        # Prepare email content
        subject = "Welcome to Our Platform!"
        html_body = f"""
        <h1>Hello {student.user.first_name},</h1>
        <p>Thank you for registering with *Career Wader* – your partner in career growth and opportunity!

        We're excited to have you on board. To complete your registration and verify your account, please use the 6-digit OTP code below:

        🔐 *Your OTP Code:* <strong>{verification_code}</strong>

        This code is valid for the next 10 minutes. Please do not share it with anyone for security reasons.

        If you did not initiate this request, please ignore this email or contact our support team.

        Welcome aboard and all the best on your career journey with us!

        Warm regards,  
        The Career Wader Team  </p>
        """

        # Send email using ZeptoMail
        email_sent, msg = send_zeptomail(
            to_email=student.user.email,
            subject=subject,
            html_body=html_body
        )

        if not email_sent:
            # Trigger rollback
            raise EmailSendFailed(detail=f"Failed to send email: {msg}")



class StudentListView(generics.ListAPIView):
    queryset = Student.objects.select_related('user').order_by('-user__created_at')
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated] # Allow public access to the list of students
    pagination_class = CustomPageNumberPagination
    filterset_class = FilterClassStudent
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['user__city', 'user__state', 'user__created_at', 'user__phone', 'user__email', 'user__first_name', 'user__last_name', 'user__country']
    
    
    def get_queryset(self):
        user = self.request.user

        # Admin/staff see all students
        if user.is_staff or user.is_superuser:
            return Student.objects.all()

        # Franchise sees only their enrolled students
        try:
            franchise = Franchise.objects.get(user=user)
            return Student.objects.filter(franchise=franchise)
        except Franchise.DoesNotExist:
            return Student.objects.none()
    
    