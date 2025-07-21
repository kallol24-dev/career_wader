from django.db import models

from account.models import User


STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('archived', 'Archived'),
    ('pending', 'Pending'),
    ('deleted', 'Deleted'),
)

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')  # Assuming you have a User model
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)  # Comma-separated tags
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # class Meta:
    #     verbose_name_plural = "Blogs"
    #     ordering = ['-created_at']  # Order by creation date, newest first