from captcha.fields import CaptchaField
from rest_framework import serializers
from captcha.models import CaptchaStore

class CaptchaVerifySerializer(serializers.Serializer):
    captcha_0 = serializers.CharField()  # CAPTCHA key
    captcha_1 = serializers.CharField()   # User-entered CAPTCHA
    
    def validate(self, data):
        key = data.get("captcha_0")
        user_input = data.get("captcha_1")

        try:
            captcha = CaptchaStore.objects.get(hashkey=key)
        except CaptchaStore.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired CAPTCHA key.")

        if captcha.response != user_input.strip().lower():
            raise serializers.ValidationError("Invalid CAPTCHA.")

        # optional: delete the CAPTCHA so it can't be reused
        captcha.delete()

        return data