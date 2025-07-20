

# Create your models here.
from django.db import models
from django.conf import settings

class Cart(models.Model):
    """
    A cart belonging to a user (likely a student).
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.email}"
    
    
class CartItem(models.Model):
    """
    An item in the cart, which can be a service.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey('service.Service', on_delete=models.CASCADE , unique=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # class Meta:
    #     unique= 'service'
    

    def __str__(self):
        return f"{self.quantity} x {self.service.name} in cart"
    
    