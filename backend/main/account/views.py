from datetime import timedelta
import json
import os
from django.utils import timezone
import random
from franchaise.models import Franchise
from franchaise.serializers import FranchiseApprovalSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, filters 

from account.utils.location import get_client_ip
from .models import User, Enquiry, ContactUs
from .serializers import UserSerializer, EnquirySerializers,VerifyEmailSerializer, ContactUsSerializer
from .permissions import  IsAdmin
from django.utils.http import urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
import requests
from rest_framework.exceptions import APIException
from django.db import transaction
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from account.utils import CITY_CODES 





class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        

        # If login is successful, set session values
        user = serializer.user
        request.session['user_id'] = user.id
        request.session['user_email'] = user.email
        request.session['user_role'] = user.role
        request.session['name'] = f"{user.first_name} {user.last_name}"
        # Print just the user_id
        print("user_id:", request.session.get('user_id'))
        # Or print all session data
        print("session data:", dict(request.session))
        
        response = super().post(request, *args, **kwargs)
        return response


class FranchiseApprovalUpdateView(generics.UpdateAPIView):
    queryset = Franchise.objects.all()
    
    serializer_class = FranchiseApprovalSerializer
    permission_classes = []  # only admin can approve

    lookup_field = 'pk'
    
    
    def generate_franchise_uuid(self,city):
        city = city.strip()
        city_code = CITY_CODES.get(city)
        print(city_code)
        if not city_code:
            raise ValueError(f"No city code found for '{city}'")

        # Get the latest franchise with that city code prefix
        last_franchise = Franchise.objects.filter(
            franchaise_uuid__startswith=f"CW{city_code}"
        ).order_by('-franchaise_uuid').first()
        print(last_franchise)
        if last_franchise:
            try:
                last_serial = int(last_franchise.franchaise_uuid[-4:])
            except (ValueError, TypeError):
                last_serial = 0
        else:
            last_serial = 0

        new_serial = f"{last_serial + 1:04d}" 
        print(f"CW{city_code}{new_serial}")# Pad with 0s
        return f"CW{city_code}{new_serial}"
    
    def perform_update(self, serializer):
        instance = serializer.instance
        was_approved = instance.is_approved  # Before update
        franchise_uuid = instance.franchaise_uuid
        print(instance.user.city)
       
        city = instance.user.city.strip()
        print("City:", city)
        code = self.generate_franchise_uuid(city)
        print(code)
        
        if not code:
            raise ValueError(f"No city code found for '{city}'")

        user = instance.user
        
        full_name = f"{user.first_name.strip()} {user.last_name.strip()}"
        # create a unique franchise UUID if not already set
        if not franchise_uuid:
            franchise_uuid = code
            instance.franchaise_uuid = franchise_uuid
            instance.save(update_fields=['franchaise_uuid'])
        # Save updated data
        updated_instance = serializer.save()

        now_approved = updated_instance.is_approved

        # Case 1: Just approved
        if not was_approved and now_approved:
            subject = "Franchise Approval - Career Wader"
            html_body = f"""
            <h2>Dear {full_name},</h2>
            <p>Congratulations! Your franchise account has been <strong>Approved</strong>.</p>
            <p> This is your Unique Identification Code {franchise_uuid}<p>
            <p>You can now log in to your dashboard and start onboarding students.</p>
            <br>
            <p>Regards,<br>Career Wader Team</p>
            """

        # Case 2: Just blocked
        elif was_approved and not now_approved:
            subject = "Franchise Account Blocked - Career Wader"
            html_body = f"""
            <h2>Dear {full_name},</h2>
            <p>Your franchise account has been <strong>blocked</strong> by the admin.</p>
            <p>You will no longer have access to your dashboard or onboarding features.</p>
            <p>If you believe this was a mistake, please contact support.</p>
            <br>
            <p>Regards,<br>Career Wader Team</p>
            """

        else:
            # No change in approval status, skip email
            return

        # Send email
        email_sent, msg = send_zeptomail(
            to_email=user.email,
            subject=subject,
            html_body=html_body
        )

        if not email_sent:
            raise EmailSendFailed(detail=f"Failed to send email: {msg}")

class AdminOnlyTestView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": f"Welcome, Admin {request.user.first_name}!"})
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]  # Only admin can access



class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)


def send_mail():
    

    url = "https://api.zeptomail.in/v1.1/email"

    payload = "{\n\"from\": { \"address\": \"noreply@tripnest.in\"},\n\"to\": [{\"email_address\": {\"address\": \"johnnongrum9@gmail.com\",\"name\": \"reiford\"}}],\n\"subject\":\"Test Email\",\n\"htmlbody\":\"<div><b> Test email sent successfully.  </b></div>\"\n}"
    headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'authorization': "Zoho-enczapikey PHtE6r1eEOq5iGIv8RgD4aS8HsOtZN97rO4xKgAWsttBWPIFTU1Uoo96wTXkrxkiVvUWQvOTzd89tbiaur+CcWvoN2cZXGqyqK3sx/VYSPOZsbq6x00asFkTc03YU4Xuc9Fv1ybfstrbNA==",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

class EmailSendFailed(APIException):
    status_code = 500
    default_detail = "Failed to send confirmation email."
    default_code = "email_send_failed"


def send_zeptomail(to_email, subject, html_body, from_email="support@careerwader.in"):
    api_url = "https://api.zeptomail.in/v1.1/email"
    api_token = "Zoho-enczapikey PHtE6r0LFLziiWItoREI5//rEsb1Pdl8+LxvKVQWuNtLX6IEHE1VqNsvmmSxoh14UKJFEPHIyt1t5bPIsrrRd2m+ZGcZX2qyqK3sx/VYSPOZsbq6x00ct14ScEHUXY7tddBq3SbVs97eNA=="
    headers = {
        "Authorization": f"{api_token}",
        "Content-Type": "application/json"
    }

    data = {
        # "bounce_address": "bounce@yourdomain.com",
        "from": {
            "address": from_email,
            "name": "Career Wader"
        },
        "to": [
            {
                "email_address": {
                    "address": to_email,
                    "name": ""
                }
            }
        ],
        "subject": subject,
        "htmlbody": html_body
    }

    response = requests.post(api_url,  json=data,headers=headers)

    if response.status_code == 201:
        return True, "Email sent successfully!"
    else:
        return False, response.text






class VerifyCodeView(generics.GenericAPIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '').strip()
        code = request.data.get('otp')

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if user.is_verification_code_valid(code):
            user.verification_code = None  # clear code
            user.verification_expiry = None
            user.save(update_fields=['verification_code', 'verification_expiry'])
            return Response({"detail": "Verification successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid or expired code."}, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationCodeView(generics.GenericAPIView):
    permission_classes = []  # Make public or restrict with rate limit

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '').strip()

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Generate a new code
        verification_code = str(random.randint(100000, 999999))
        expiry_minutes = 10

        user.verification_code = verification_code
        user.verification_expiry = timezone.now() + timezone.timedelta(minutes=expiry_minutes)
        user.save(update_fields=['verification_code', 'verification_expiry'])

        # Send email
        subject = "Your Verification Code"
        html_body = f"""
        <h1>Hello {user.first_name},</h1>
        <p>Your new verification code is: <b>{verification_code}</b></p>
        <p>This code will expire in {expiry_minutes} minutes.</p>
        """

        email_sent, msg = send_zeptomail(
            to_email=user.email,
            subject=subject,
            html_body=html_body
        )

        if not email_sent:
            return Response({"detail": f"Failed to send email: {msg}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": "Verification code resent successfully."}, status=status.HTTP_200_OK)

class ForgotPasswordRequest(generics.GenericAPIView):
    permission_classes = []  # Make public or restrict with rate limit

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '').strip()

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Generate Django reset token
        token = PasswordResetTokenGenerator().make_token(user)

        # Example: generate frontend reset URL
        reset_url = f"{settings.FRONTEND_URL}/confirm-reset-password?uid={user.id}&token={token}"

        # Prepare email
        subject = "Reset Your Password"
        html_body = f"""
        <h1>Hello {user.first_name},</h1>
        <p>We received a request to reset your password.</p>
        <p>Click the link below to reset your password:</p>
        <p><a href="{reset_url}">{reset_url}</a></p>
        <p>This link will expire in a limited time. If you didn’t request this, please ignore this email.</p>
        """

        # Send email
        email_sent, msg = send_zeptomail(
            to_email=user.email,
            subject=subject,
            html_body=html_body
        )

        if not email_sent:
            return Response({"detail": f"Failed to send email: {msg}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": "Verification code resent successfully."}, status=status.HTTP_200_OK)



class ResetPasswordView(generics.GenericAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not uid or not token or not new_password:
            return Response({"detail": "uid, token, and new_password are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            return Response({"detail": "Invalid user."}, status=status.HTTP_404_NOT_FOUND)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:
            return Response({"detail": "Password must be at least 8 characters."},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)
# class FranchiseRegisterView(generics.CreateAPIView):
#     queryset = Franchise.objects.all()
#     serializer_class = FranchiseSerializer
#     permission_classes = []  # Allow public registration
    
#     @transaction.atomic
#     def perform_create(self, serializer):
#         franchise = serializer.save()
#         user = franchise.user
#         print(user.first_name)
        
        
        
        
#         # Generate 6-digit code
#         verification_code = str(random.randint(100000, 999999))

#         # Set expiry time to 10 minutes from now
#         expiry_time = timezone.now() + timedelta(minutes=10)

#         # Save to user
#         user.verification_code = verification_code
#         user.verification_expiry = expiry_time
#         user.save(update_fields=['verification_code', 'verification_expiry'])
        

#         # Prepare email content
#         subject = "Welcome to Our Platform!"
#         html_body = f"""
#         <h1>Hello {franchise.user.first_name},</h1>
#         <p>Thank you for registering with *Career Wader* – your partner in career growth and opportunity!

#         We're excited to have you on board. To complete your registration and verify your account, please use the 6-digit OTP code below:

#         🔐 *Your OTP Code:* <strong>{verification_code}</strong>

#         This code is valid for the next 10 minutes. Please do not share it with anyone for security reasons.

#         If you did not initiate this request, please ignore this email or contact our support team.

#         Welcome aboard and all the best on your career journey with us!

#         Warm regards,  
#         The Career Wader Team  </p>
#         """

#         # Send email using ZeptoMail
#         email_sent, msg = send_zeptomail(
#             to_email=franchise.user.email,
#             subject=subject,
#             html_body=html_body
#         )

#         if not email_sent:
#             # Trigger rollback
#             raise EmailSendFailed(detail=f"Failed to send email: {msg}")



# class CounselorViewSet(viewsets.ModelViewSet):
#     """
#     Handles List, Create, Retrieve, Update, and Delete for Counselor.
#     """
#     queryset = Counselor.objects.all()
#     serializer_class = CounselorSerializer

#     def get_permissions(self):
#         """Apply different permissions for list, create, update, and delete."""
#         if self.action in ["create","update", "partial_update"]:
#             return [permissions.AllowAny()]  # Allow all authenticated users
#         elif self.action in ["list","create", "update", "partial_update", "destroy"]:
#             return [permissions.IsAdminUser()]  # Restrict modifications to Admins only
#         return []
#     def perform_create(self, serializer):
#         """Ensure the linked user is created with the correct role"""
#         serializer.save()

class EnquiryCreate(generics.CreateAPIView):
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializers
    permission_classes = []
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            {"message": "Enquiry submitted successfully"},
            status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        serializer.save()

class EnquiryView(generics.ListAPIView):
    
    # queryset = Enquiry.objects.all().order_by('-id')
    serializer_class = EnquirySerializers
    permission_classes = [IsAdmin]  # Only admin can access
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['state', 'city', 'created_at']
    search_fields = ['city', 'state', 'created_at', 'phone_number', 'email', 'full_name', 'message']
    
    def get_queryset(self):
        status = self.request.query_params.get('status')
        queryset = Enquiry.objects.all().order_by('-id')

        if status == 'unread':
            return queryset.filter(is_read=False)
        elif status == 'read':
            return queryset.filter(is_read=True)

        return queryset
    

class MarkEnquiryReadView(APIView):
    permission_classes = [IsAdmin]  # Or IsAdminUser if using Django default

    def patch(self, request, pk):
        try:
            enquiry = Enquiry.objects.get(pk=pk)
        except Enquiry.DoesNotExist:
            return Response({"error": "Enquiry not found"}, status=status.HTTP_404_NOT_FOUND)

        enquiry.is_read = True
        enquiry.save()
        return Response({"message": "Enquiry marked as read"}, status=status.HTTP_200_OK)
class MarkContactUsReadView(APIView):
    permission_classes = [IsAdmin]  # Or IsAdminUser if using Django default

    def patch(self, request, pk):
        try:
            enquiry = ContactUs.objects.get(pk=pk)
        except ContactUs.DoesNotExist:
            return Response({"error": "Contact not found"}, status=status.HTTP_404_NOT_FOUND)

        enquiry.is_read = True
        enquiry.save()
        return Response({"message": "Contact marked as read"}, status=status.HTTP_200_OK)

class ContactUsCreateView(generics.CreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = []
class ContactUsListView(generics.ListAPIView):
    queryset = ContactUs.objects.all().order_by('-id')
    serializer_class = ContactUsSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['state', 'city', 'created_at']
    search_fields = ['city', 'state', 'created_at', 'phone_number', 'email', 'first_name', 'last_name', 'message']
    
    def get_queryset(self):
        status = self.request.query_params.get('status')
        queryset = ContactUs.objects.all().order_by('-id')

        if status == 'unread':
            return queryset.filter(is_read=False)
        elif status == 'read':
            return queryset.filter(is_read=True)

        return queryset
    
    

