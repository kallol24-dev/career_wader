from django.contrib.auth.models import AbstractUser ,BaseUserManager
from django.db import models 
from django.utils.timezone import now, timedelta
import random
import string
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import Group


class UserManager(BaseUserManager):
    def create_user(self, email, password=None,role=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        if role:
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)
        return user

    # def create_superuser(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault("is_staff", True)
    #     extra_fields.setdefault("is_superuser", True)
    #     extra_fields.setdefault('role', 'Admin') 
        
    #     return self.create_user(email, password, **extra_fields)
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        user = self.create_user(email, password, role="Admin", **extra_fields)
        return user
    

    



class User(AbstractUser):

    username = None  # Remove default username field
    email = models.EmailField(unique=True)  # Use email as the unique identifier
    phone = models.CharField(max_length=15, unique=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_expiry = models.DateTimeField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    
    # ROLE_CHOICES = (
    #     ("student", "Student"),
    #     ("counselor", "Counselor"),
    #     ("admin", "Admin"),
    #     ("franchise", "Franchise"),
    # )
    COUNTRY_CHOICES =(
        ("IN","India"),
        ("ID","Indonesia"),
        ("IR","Iran"),
        ("HU","Hungary"),
    )
    # role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    @property
    def role(self):
        group = self.groups.first()
        return group.name if group else None
    
    
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default="IN")

    USERNAME_FIELD = "email"  # Use email as the authentication field
    REQUIRED_FIELDS = ["first_name", "last_name", "phone", "country"]

    def generate_verification_code(self):
            """Generate a 6-digit random verification code."""
            self.verification_code = "".join(random.choices(string.digits, k=6))
            self.verification_expiry = now() + timedelta(minutes=10)  # Expires in 10 mins
            self.save()

    objects = UserManager() 
    
    def is_verification_code_valid(self, code):
        return (
            self.verification_code == code and
            self.verification_expiry and
            timezone.now() <= self.verification_expiry
        )





    

# class Counselor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="counselor")
    

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin")





class Enquiry(models.Model):
    
    # CATEGORY_CHOICES = (
    #     ("Student", "Student"),
    #     ("Faculty", "Faculty"),
    #     ("Counselor", "Counselor"),
    #     ("Executive", "Executive"),
    #     ("Franchise", "Franchise"),
    #     ("Others", "Others"),
    # )
    
    
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    form_submitted_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    # Add city field
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    
    is_read = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["full_name", "phone_number","message", "city", "email", "state"]
    
    
class ContactUs(models.Model):
    
    
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        email = models.EmailField()
        phone_number = models.CharField(max_length=10)
        message = models.TextField()
        ip_address = models.GenericIPAddressField(null=True, blank=True)
        created_at = models.DateTimeField(auto_now_add=True, blank=True)
        updated_at = models.DateTimeField(auto_now=True, blank=True)
        
        is_read = models.BooleanField(default=False)
        city = models.CharField(max_length=100, null=True, blank=True)
        state = models.CharField(max_length=100, null=True, blank=True)
        

        REQUIRED_FIELDS = ["first_name", "last_name", "phone_number", "message", "email", "city", "state"]
