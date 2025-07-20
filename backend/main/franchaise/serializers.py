from account.serializers import UserSerializer
from .models import Franchise, FranchiseTask
from rest_framework import serializers
from account.models import User

class FranchiseSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model =Franchise
        fields = ["user","is_approved", "id"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        role = user_data.pop("role", "franchise") 
        print (role);
        user = User.objects.create_user(**user_data, role=role)
        franchise = Franchise.objects.create(user=user, **validated_data)
        return franchise


class FranchiseApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        fields = ['is_approved', 'franchaise_uuid']

class ShortlistByCitySerializer(serializers.Serializer):
    city = serializers.CharField(required=True)


class AdminFranchiseActionSerializer(serializers.Serializer):
    franchise_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=["SHORTLISTED", "REJECTED"])
    
# form for updating farainchise tasks 
class FranchiseTaskUpdateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = FranchiseTask
        fields = '__all__'
        read_only_fields = ['user']
       
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)