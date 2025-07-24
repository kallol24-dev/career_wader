
from rest_framework import serializers
from .models import EducationLoan


class EducationLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLoan
        fields = '__all__'