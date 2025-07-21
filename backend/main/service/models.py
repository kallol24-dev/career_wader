from django.db import models


class ServiceType(models.Model):
    """
    Model to represent different types of services.
    """
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_avaiable = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    

    def __str__(self):
        return self.name
# Create your models here.
class Service(models.Model):
    """
    Model to represent a service.
    """
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type.name}: {self.name}"
    