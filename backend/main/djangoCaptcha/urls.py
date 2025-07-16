from django.urls import path
from .views import CaptchaVerifyAPIView, CaptchaRefreshAPIView

urlpatterns = [
    path("refresh/", CaptchaRefreshAPIView.as_view(), name="captcha-refresh"),
    path("verify/", CaptchaVerifyAPIView.as_view(), name="captcha-verify"),
]