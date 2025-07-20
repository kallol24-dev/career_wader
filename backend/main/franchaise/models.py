from django.db import models

from account.models import Admin, User
from django.conf import settings

# Create your models here.
class Franchise(models.Model):
    
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SHORTLISTED", "Shortlisted"),
        ("REJECTED", "Rejected"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="franchise")
    is_approved = models.BooleanField(default=False)
    
    city = models.CharField(max_length=100)
    franchaise_uuid = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    is_shortlisted = models.BooleanField(default=False)
    shortlisted_at = models.DateTimeField(null=True, blank=True)
    shortlisted_by = models.ForeignKey(Admin, null=True, blank=True, on_delete=models.SET_NULL, related_name="shortlisted_franchises")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True )

    def __str__(self):
        return f"{self.user.email} ({self.city})"
    

class FranchiseTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="franchise_tasks")
    TASK_STATUS_CHOICE = [
        ('NOT INTERESTED', 'not interested'),
        ('INTERESTED', 'interested'),
        ('PENDING','pending'),
        ('COMPLETED', 'completed'),
        ('FOLLOW UP', 'follow up'),
        
    ]
    
    
    
    lead_title = models.CharField(max_length=100)
    progress_status =  models.CharField(max_length=100)
    comments = models.TextField(max_length=150)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICE, default="PENDING")
    source = models.CharField(max_length=100)
    interested_service = models.CharField(max_length=100)
    follow_up_dates = models.DateTimeField(null=True, blank=True)
    description = models.TextField(max_length=150)
    # Fields to be updated by admin only
    notes = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
