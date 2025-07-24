from django.shortcuts import render
from rest_framework import generics, permissions
from .models import EducationLoan
from .serializers import EducationLoanSerializer
# Create your views here.
class EducationLoanListView(generics.ListAPIView):
    queryset = EducationLoan.objects.all()
    serializer_class = EducationLoanSerializer
    permission_classes = [permissions.IsAdminUser]
    
    
    
    
class EducationLoanCreateView(generics.CreateAPIView):
    queryset = EducationLoan.objects.all()
    serializer_class = EducationLoanSerializer
    permission_classes = [permissions.AllowAny]

class EducationLoanDetailView(generics.RetrieveAPIView):
    queryset = EducationLoan.objects.all()
    serializer_class = EducationLoanSerializer
    permission_classes = [permissions.IsAdminUser]

class EducationLoanUpdateView(generics.UpdateAPIView):
    queryset = EducationLoan.objects.all()
    serializer_class = EducationLoanSerializer
    permission_classes = [permissions.IsAdminUser]

class EducationLoanDeleteView(generics.DestroyAPIView):
    queryset = EducationLoan.objects.all()
    serializer_class = EducationLoanSerializer
    permission_classes = [permissions.IsAdminUser]