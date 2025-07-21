from franchaise.serializers import FranchiseSerializer
from rest_framework import serializers
from account.serializers import UserSerializer
from checkout.serializers import checkoutSerializer
from account.models import User
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    checkout = checkoutSerializer(many=True, read_only=True, source='checkouts')
    franchise = FranchiseSerializer(read_only=True)

    class Meta:
        model =Student
        fields = ["user", "franchise", "checkout"]
    def get_franchise(self, obj):
    # Prevent error if obj is a plain dict (e.g., unsaved or during creation)
        if isinstance(obj, dict):
            return None

        if hasattr(obj, 'franchise') and obj.franchise:
            return FranchiseSerializer(obj.franchise).data
        return None
    
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        # role = user_data.pop("role", "Student")
        role = "Student"
        print (role);
        user = User.objects.create_user(**user_data, role=role)
        student = Student.objects.create(user=user, **validated_data)
        return student
    