

from account.models import User
from account.serializers import UserSerializer
from .models import CounselingSession, Counselor, Counselor_background, CounselorFeedback
from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings



class CounselorBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counselor_background
        exclude = ['counselor'] 



# class CounselorSerializer(serializers.ModelSerializer):
#     user = UserSerializer()  
#     background = CounselorBackgroundSerializer(many=True, required=False)

#     class Meta:
#         model = Counselor
#         fields = ["id","user","current_occupation","experience_in_years","is_terms_agreed","is_approved","background"]

#     # def create(self, validated_data):
#     #     print(self.request.)
#     #     user_data = validated_data.pop("user")
#     #     background_data = validated_data.pop("background", [])
#     #     role = user_data.pop("role", "counselor") 
#     #     # print (role);
#     #     user = User.objects.create_user(**user_data, role=role)
#     #     user.generate_verification_code()
#     #     counselor = Counselor.objects.create(user=user, **validated_data)
        
#     #     # Create background(s)
#     #     for bg in background_data:
#     #         Counselor_background.objects.create(counselor=counselor, **bg)

#     #     # Send email
#     #     send_mail(
#     #         "Your Verification Code",
#     #         f"Your verification code is: {user.verification_code}",
#     #         settings.DEFAULT_FROM_EMAIL,
#     #         [user.email],
#     #         fail_silently=False,
#     #     )  # ✅ Send email verification
#     #     return counselor
#     def create(self, validated_data):
#         request = self.context.get('request')
#         user_data = validated_data.pop("user")
#         background_data = validated_data.pop("background", [])

#         role = user_data.pop("role", "counselor")
#         user = User.objects.create_user(**user_data, role=role)
#         user.generate_verification_code()

#         counselor = Counselor.objects.create(user=user, **validated_data)

#         for index, bg in enumerate(background_data):
#             file_field_key = f"background[{index}][certification_qualification]"
#             file = request.FILES.get(file_field_key)

#             Counselor_background.objects.create(
#                 counselor=counselor,
#                 certification_qualification=file,
#                 counselling_specialization=bg.get("counselling_specialization", ""),
#                 relevant_exp=bg.get("relevant_exp", 0)
#             )

#             return counselor
    



class CounselorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    background = CounselorBackgroundSerializer(many=True, required=False)

    class Meta:
        model = Counselor
        fields = [
            "id", "user", "current_occupation", "experience_in_years","motivation_reason","hope_reason",
            "is_terms_agreed", "is_approved", "background"
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        user_data = validated_data.pop("user")
        background_data = validated_data.pop("background", [])

        # Create user
        role = user_data.pop("role", "counselor")
        user = User.objects.create_user(**user_data, role=role)
        user.generate_verification_code()

        # Create counselor
        counselor = Counselor.objects.create(user=user, **validated_data)

        # Create background records
        for index, bg in enumerate(background_data):
            file_field_key = f"background[{index}][certification_qualification]"
            file = request.FILES.get(file_field_key)

            Counselor_background.objects.create(
                counselor=counselor,
                certification_qualification=file,
                counselling_specialization=bg.get("counselling_specialization", ""),
                relevant_exp=bg.get("relevant_exp", 0)
            )

        # Optional: send verification email
        # send_mail(
        #     "Your Verification Code",
        #     f"Your verification code is: {user.verification_code}",
        #     settings.DEFAULT_FROM_EMAIL,
        #     [user.email],
        #     fail_silently=False,
        # )

        return counselor

class CounselingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselingSession
        fields = '__all__'
        # read_only_fields = ['counselor', 'session_date']

class CounselingSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselingSession
        fields = ['student', 'counselor','counselor_notes', 'action_plan', 'follow_up_date']
        read_only_fields = ['counselor', 'session_date']

    def create(self, validated_data):
        counselor = self.context['request'].user.counselor if hasattr(self.context['request'].user, 'counselor') else None
        validated_data['counselor'] = counselor
        return super().create(validated_data)

class CounselorFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselorFeedback
        fields = '__all__'
        read_only_fields = ['counselor', 'session']
    
    def create(self, validated_data):
        session = validated_data.get('session')
        counselor = session.counselor if session else None
        validated_data['counselor'] = counselor
        return super().create(validated_data)