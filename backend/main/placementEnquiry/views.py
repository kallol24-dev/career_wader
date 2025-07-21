from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import PlacementEnquiry
from .serializers import PlacementEnquirySerializer

class PlacementEnquiryListCreateView(generics.ListCreateAPIView):
    serializer_class = PlacementEnquirySerializer
    queryset = PlacementEnquiry.objects.all().order_by('-created_at')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]