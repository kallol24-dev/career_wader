from datetime import timedelta
from django.utils import timezone
import random
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, permissions, viewsets
from .models import User, Counselor, Enquiry
from .serializers import UserSerializer, CounselorSerializer, EnquirySerializers,VerifyEmailSerializer
from .permissions import IsStudent, IsCounselor, IsAdmin
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



class CounselorViewSet(viewsets.ModelViewSet):
    """
    Handles List, Create, Retrieve, Update, and Delete for Counselor.
    """
    queryset = Counselor.objects.all()
    serializer_class = CounselorSerializer

    def get_permissions(self):
        """Apply different permissions for list, create, update, and delete."""
        if self.action in ["create","update", "partial_update"]:
            return [permissions.AllowAny()]  # Allow all authenticated users
        elif self.action in ["list","create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]  # Restrict modifications to Admins only
        return []
    def perform_create(self, serializer):
        """Ensure the linked user is created with the correct role"""
        serializer.save()

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
    queryset = Enquiry.objects.all().order_by('created_at')
    serializer_class = EnquirySerializers
    permission_classes = [IsAdmin]

