from django.db import models

# Create your models here.
class EducationLoan(models.Model):
    name= models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    prefered_destination = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    loan_amount = models.CharField(max_length=100)
    is_terms_agreed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)