from django.db import models

# Create your models here.
class Checkout(models.Model):
    """
    Represents a checkout process for a user.
    """
    service = models.ForeignKey('service.Service', on_delete=models.CASCADE)
    franchaise_uuid = models.ForeignKey(
        'franchaise.Franchise',
        to_field='franchaise_uuid',  # 👈 Refers to the unique CharField
        on_delete=models.CASCADE,
        related_name='checkouts',
        blank=True,
        null=True
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=10 , blank=True, null=True)
    