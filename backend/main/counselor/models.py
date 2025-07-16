from django.db import models

from account.models import User
from student.models import Student

# Create your models here.
class Counselor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="counselor")
    current_occupation = models.CharField(max_length=100 , blank=True, null=True)
    experience_in_years = models.IntegerField(blank=True, null=True)
    is_terms_agreed = models.BooleanField(default=False)
    motivation_reason = models.TextField( blank=True, null=True)
    hope_reason = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    
    

class Counselor_background(models.Model):
    counselor =  models.ForeignKey(Counselor, on_delete=models.CASCADE, related_name='background')
    counselling_specialization = models.TextField()
    certification_qualification = models.ImageField(upload_to='certifications/')
    relevant_exp = models.IntegerField()
    
    


class CounselingSession(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='sessions')
    counselor = models.ForeignKey(Counselor, on_delete=models.SET_NULL, null=True, related_name='sessions')
    session_date = models.DateField(auto_now_add=True)
    issues_discussed = models.TextField()
    counselor_notes = models.TextField()
    action_plan = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Session with {self.student.user.get_full_name()} on {self.session_date}"
    

class CounselorFeedback(models.Model):
    session = models.ForeignKey(CounselingSession, on_delete=models.CASCADE, related_name='feedback')
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_date = models.DateField(auto_now_add=True)
    feedback_text = models.TextField()
    feedback_report = models.FileField(upload_to='feedback_reports/', null=True, blank=True)

    def __str__(self):
        return f"Feedback for session {self.session.id} by {self.counselor.user.get_full_name()}"