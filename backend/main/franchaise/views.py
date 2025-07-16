
import random
import string
from django.shortcuts import render
from account.models import Admin, User
from main.pagination import CustomPageNumberPagination
from rest_framework import generics, filters,status, permissions,serializers
from rest_framework.exceptions import APIException
from django.db import transaction
from datetime import timedelta

from django.utils import timezone

from account.views import EmailSendFailed
from student.models import Student
from student.serializers import StudentSerializer
from .models import Franchise
from .serializers import AdminFranchiseActionSerializer, FranchiseSerializer, ShortlistByCitySerializer
from account.views import send_zeptomail
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from franchaise.filters import FilterClassFranchise

# Create your views here.
class FranchiseListView(generics.ListAPIView):
    # queryset = Franchise.objects.all()
    
    queryset = Franchise.objects.select_related('user').all().order_by('-id')
    serializer_class = FranchiseSerializer
    permission_classes = [permissions.IsAdminUser] 
    pagination_class = CustomPageNumberPagination
    
    # filterset_fields = ['user__state', 'user__city', 'user__created_at', 'user__country']
    filterset_class = FilterClassFranchise
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['is_approved','user__city', 'user__state', 'user__created_at', 'user__phone', 'user__email', 'user__first_name', 'user__last_name', 'user__country']
    
    
    
class FranchiseRegisterView(generics.CreateAPIView):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer
    permission_classes = []  # Allow public registration
    
    @transaction.atomic
    def perform_create(self, serializer):
        franchise = serializer.save()
        user = franchise.user
        print(user.first_name)
        
        
        
        
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
        <h1>Hello {franchise.user.first_name},</h1>
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
            to_email=franchise.user.email,
            subject=subject,
            html_body=html_body
        )

        if not email_sent:
            # Trigger rollback
            raise EmailSendFailed(detail=f"Failed to send email: {msg}")




class FranchiseStudentRegisterView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        franchise_user = self.request.user

        try:
            franchise = franchise_user.franchise
        except AttributeError:
            raise serializers.ValidationError("You are not a registered franchise.")

        # Extract data manually from context (not validated_data)
        request_data = self.request.data['user']
        email = request_data.get('email')
        first_name = request_data.get('first_name')
        last_name = request_data.get('last_name')
        # phone = request_data.get('phone')
        # country=self.request.data.get('country', 'IN'),
        # city=self.request.data.get('city', ''),
        # state=self.request.data.get('state', '')
        print(request_data)
        if not email or not first_name or not last_name:
            raise serializers.ValidationError("email, first_name, and last_name are required.")

        # random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        password = request_data.get('password') or ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        print(password)

        # Create the User
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            phone=request_data.get('phone'),
            is_active=True,
            country=request_data.get('country', 'IN'),
            city=request_data.get('city', ''),
            state=request_data.get('state', '')
        )
       
        
        # Now save the Student linked to the franchise and user
        student = Student.objects.create(user=user, franchise=franchise)

        # Send credentials via email
        subject = "Welcome to Career Wader – Your Login Credentials"
        # html_body = f"""
        # <h2>Hello {first_name},</h2>
        # <p>You have been registered as a student on <strong>Career Wader</strong> by your franchise.</p>
        # <p><strong>Here are your login credentials:</strong></p>
        # <ul>
        #     <li>Email: <strong>{email}</strong></li>
        #     <li>Password: <strong>{password}</strong></li>
        # </ul>
        # <p>We recommend you log in and change your password immediately.</p>
        # <br>
        # <p>Best of luck on your journey!<br>The Career Wader Team</p>
        # """
        html_body = f"""
        <h2>Hello {first_name},</h2>
        <p>You have been registered as a student on <strong>Career Wader</strong> by your franchise.</p>
        
        <p>We recommend you to click the link below and take the Career Counselling test</p>
        <Button><a href="https://www.careertest.careerwader.in/general/careerTest">Take the Career Counselling Test</a></Button>
        <br>
        <p>Best of luck on your journey!<br>The Career Wader Team</p>
        """
        email_sent, msg = send_zeptomail(
            to_email=email,
            subject=subject,
            html_body=html_body
        )

        if not email_sent:
            raise EmailSendFailed(detail=f"Failed to send email: {msg}")





class ShortlistFranchisesByCityView(generics.GenericAPIView):
    serializer_class = ShortlistByCitySerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = CustomPageNumberPagination

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        city = serializer.validated_data['city']

        try:
            admin = Admin.objects.get(user=request.user)
        except Admin.DoesNotExist:
            return Response({"detail": "Only admins can perform this action."}, status=status.HTTP_403_FORBIDDEN)

        franchises = Franchise.objects.filter(city__iexact=city, is_shortlisted=False)

        if not franchises.exists():
            return Response({"detail": f"No unshortlisted franchises found in {city}."}, status=status.HTTP_404_NOT_FOUND)

        count = franchises.update(
            is_shortlisted=True,
            shortlisted_at=timezone.now(),
            shortlisted_by=admin
        )

        return Response({"detail": f"{count} franchises in {city} shortlisted successfully."}, status=status.HTTP_200_OK)

class AdminFranchiseActionView(generics.GenericAPIView):
    serializer_class = AdminFranchiseActionSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        franchise_id = serializer.validated_data["franchise_id"]
        action = serializer.validated_data["action"]

        try:
            franchise = Franchise.objects.get(id=franchise_id)
        except Franchise.DoesNotExist:
            return Response({"detail": "Franchise not found."}, status=status.HTTP_404_NOT_FOUND)

        admin = Admin.objects.get(user=request.user)

        franchise.status = action
        franchise.updated_by = admin
        franchise.save()

        return Response({
            "detail": f"Franchise has been marked as {action.lower()}."
        }, status=status.HTTP_200_OK)

# create  a view for creating uuid for franchise
class FranchiseUUIDCreateView(generics.CreateAPIView):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        franchise = serializer.save()
        # Generate a unique UUID for the franchise
        franchise.franchaise_uuid = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        franchise.save(update_fields=['franchaise_uuid'])
        return franchise