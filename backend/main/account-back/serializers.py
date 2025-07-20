


from rest_framework import serializers

from account.utils.location import get_client_ip
from .models import  Counselor, Enquiry
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import send_mail
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth import get_user_model




User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        return token
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom fields to the response payload
        data["role"] = self.user.role
        data["email"] = self.user.email
        data["id"] = self.user.id  # Optional: user ID

        return data


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "country", "password","is_active","role"]
        read_only_fields = ["role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    def get_role(self, obj):
        print("Groups for user:", obj.groups.all())
        return obj.groups.first().name if obj.groups.exists() else None
    



# class FranchiseSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     class Meta:
#         model =Franchise
#         fields = ["user"]
    
#     def create(self, validated_data):
#         user_data = validated_data.pop("user")
#         role = user_data.pop("role", "franchise") 
#         print (role);
#         user = User.objects.create_user(**user_data, role=role)
#         franchise = Franchise.objects.create(user=user, **validated_data)
#         return franchise


# class StudentSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     class Meta:
#         model =Student
#         fields = ["user"]
    
#     def create(self, validated_data):
#         user_data = validated_data.pop("user")
#         role = user_data.pop("role", "student") 
#         print (role);
#         user = User.objects.create_user(**user_data, role=role)
#         student = Student.objects.create(user=user, **validated_data)
#         return student
    

class CounselorSerializer(serializers.ModelSerializer):
    user = UserSerializer()  

    class Meta:
        model = Counselor
        fields = ["id","user"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        role = user_data.pop("role", "counselor") 
        user = User.objects.create_user(**user_data, role=role)
        user.generate_verification_code()
        counselor = Counselor.objects.create(user=user, **validated_data)
        


        # Send email
        send_mail(
            "Your Verification Code",
            f"Your verification code is: {user.verification_code}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )  # ✅ Send email verification
        return counselor
    
class EnquirySerializers(serializers.ModelSerializer):  # Use ModelSerializer
    ip_address = serializers.CharField(read_only=True)
    form_submitted_url = serializers.URLField(read_only=True, required=False)
    class Meta:
        model = Enquiry
        fields = ["full_name", "email", "phone_number", "message", "city", "ip_address", "form_submitted_url"]

    def create(self, validated_data):
        request = self.context.get('request')
        ip = get_client_ip(request) if request else None
        submitted_url = request.data.get("form_submitted_url") if request else None
        # print("Request data:", request.data.get("form_submitted_url"))
        validated_data['form_submitted_url'] = submitted_url
        validated_data['ip_address'] = ip
        return Enquiry.objects.create(**validated_data)  
    



class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"], verification_code=data["code"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid code or email.")

        if user.verification_expiry and user.verification_expiry < now():
            raise serializers.ValidationError("Verification code has expired.")

        user.is_verified = True
        user.verification_code = None  # Clear the code
        user.verification_expiry = None
        user.save()
        return data
