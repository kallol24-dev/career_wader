from django.urls import path
from .views import PlacementEnquiryListCreateView

urlpatterns = [
    path('', PlacementEnquiryListCreateView.as_view(), name='placement-enquiries'),
]