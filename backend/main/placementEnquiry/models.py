from django.db import models

# Create your models here.
class PlacementEnquiry(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=13)
    city = models.CharField(max_length=13)
    preferred_destination = models.CharField()
    nearest_office = models.CharField(max_length=100, blank=True, null=True)
    is_coaching = models.BooleanField(default=False)
    is_loan = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    