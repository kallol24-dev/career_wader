from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CaptchaVerifySerializer
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from rest_framework import permissions

class CaptchaRefreshAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kwargs):
        new_key = CaptchaStore.generate_key()
        image_url = captcha_image_url(new_key)
        return Response({
            "key": new_key,
            "image_url": image_url
        })


class CaptchaVerifyAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = CaptchaVerifySerializer(data=request.data)
        if serializer.is_valid():
            return Response({"success": True})
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)