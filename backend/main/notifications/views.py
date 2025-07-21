
from .models import Notification
from rest_framework import generics 
from rest_framework import permissions as permission
from .serializers import NotificationSerializer

# Create your views here.
class NotificationsListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    queryset  = Notification.objects.all()
    permission_class = [permission.IsAdminUser]
    

    