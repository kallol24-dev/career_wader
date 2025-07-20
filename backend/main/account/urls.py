
# from django.contrib import admin
# from django.urls import path
# from rest_framework_simplejwt.views import TokenVerifyView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
# ]

from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from account.views import UserListView, StudentRegisterView, CounselorRegisterView, StudentListView, CounselorListView
from account import views
from account.serializers import CustomTokenObtainPairSerializer
from .views import AdminOnlyTestView, CustomTokenObtainPairView




urlpatterns = [
    
    
    
    
    
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path("api/users/", views.UserListView.as_view(), name="user-list"),


    # Student API
    #  path("api/students/register/", views.StudentRegisterView.as_view(), name="student-register"),
    #  path("api/students/", views.StudentListView.as_view(), name="students-list"),
      
      #  Auth Urls
     path("api/verifyemail/", views.VerifyCodeView.as_view(), name="studentemail-verification"),
     path('api/resendotp/', views.ResendVerificationCodeView.as_view(), name='resend-verification-code'),
     path('api/forgot-password/', views.ForgotPasswordRequest.as_view(), name='forgot-password'),
     path('api/reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    
    
    # Franchise API
    #  path("api/franchise/register/", views.FranchiseRegisterView.as_view(), name="franchise-register"),
    #  path("api/franchise/", views.FranchiseListView.as_view(), name="franchise-list"),
    #Admin approval
     path('api/franchise/approval/<int:pk>/', views.FranchiseApprovalUpdateView.as_view(), name='franchise-approval'),
        
     path('api/enquiries/<int:pk>/mark-read/', views.MarkEnquiryReadView.as_view(), name='enquiry-mark-read'),
     path('api/contact/<int:pk>/mark-read/', views.MarkContactUsReadView.as_view(), name='contact-mark-read'),


    # Enquiry Form
    path("api/enquiry/post/", views.EnquiryCreate.as_view(), name="enquiry-post"),
    path("api/enquiry/", views.EnquiryView.as_view(), name="enquiry-view"),
    path("verify-email/", views.VerifyEmailView.as_view(), name="verify-email"),
    
    path("api/contactus/", views.ContactUsListView.as_view(), name="contact-us"),
    path("api/contactus/post/", views.ContactUsCreateView.as_view(), name="contact-us-create"),


    # JWT authentication endpoints
    # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),


    
]
