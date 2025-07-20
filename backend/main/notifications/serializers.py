from rest_framework import serializers

from account.serializers import UserSerializer
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y")
    sender  = UserSerializer(read_only=True)
    franchaise_uuid = serializers.SerializerMethodField()
    class Meta:
        model = Notification
        fields = ['id',  'message','file', 'created_at','franchaise_uuid','sender', 'is_read']

    def get_franchaise_uuid(self, obj):
        try:
            return str(obj.sender.franchise.franchaise_uuid)  # ✅ Correct
        except AttributeError:
            return None
    