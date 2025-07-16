from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from franchaise.models import Franchise
from service.models import Service

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Student")
    franchise = models.ForeignKey(Franchise, on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name="student_service")
    checkout = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name="student_checkout")