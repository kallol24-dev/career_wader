from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class TestType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='test_types')

    def __str__(self):
        return self.name

class Question(models.Model):
    USER_GROUP_CHOICES = [
        ('class_8_10', 'Class 8–10'),
        ('class_11_12', 'Class 11–12'),
        ('college', 'College Students'),
        ('working', 'Working Professionals'),
    ]
    
   

    question = models.TextField()
    category = models.ForeignKey(TestType, on_delete=models.CASCADE, related_name="questions")
    user_group = models.CharField(max_length=20, choices=USER_GROUP_CHOICES)
    order = models.PositiveIntegerField(default=0)
    
     # Options A-D (text or image)
    option_a_text = models.CharField(max_length=255, blank=True, null=True)
    option_a_image = models.ImageField(upload_to='option_images/', blank=True, null=True)

    option_b_text = models.CharField(max_length=255, blank=True, null=True)
    option_b_image = models.ImageField(upload_to='option_images/', blank=True, null=True)

    option_c_text = models.CharField(max_length=255, blank=True, null=True)
    option_c_image = models.ImageField(upload_to='option_images/', blank=True, null=True)

    option_d_text = models.CharField(max_length=255, blank=True, null=True)
    option_d_image = models.ImageField(upload_to='option_images/', blank=True, null=True)
    
    option_e_text = models.CharField(max_length=255, blank=True, null=True)
    option_e_image = models.ImageField(upload_to='option_images/', blank=True, null=True)
    
    option_f_text = models.CharField(max_length=255, blank=True, null=True)
    option_f_image = models.ImageField(upload_to='option_images/', blank=True, null=True)

    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'),('F','F')
    ])

    def __str__(self):
        return f"{self.user_group} - {self.order}. {self.text}"