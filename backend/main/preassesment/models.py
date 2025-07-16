from django.db import models
from django.conf import settings

from account.models import User
# Create your models here.
class PreAssesment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preassesment")
    fathers_name = models.CharField(max_length=100)
    mothers_name = models.CharField(max_length=100)
    siblings_no = models.IntegerField(default=0, blank=True)
    family_occupation = models.CharField(max_length=100) 
    
    # Academic Background
    highest_qualification = models.TextField(help_text="Comma Seperated values")
    relevant_subject = models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    performance_levels = models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    
    
    #Academic Achievements:
    scolarships = models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    award_recognition = models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    strengths = models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    weaknesses = models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    
    #Extracurricular Activities
    hobbies = models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    sports = models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    voluntary_experiences = models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    other_relevant_experiences = models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    
    #Interests and Values
    career_related_interests = models.TextField(help_text="Comma Seperated values")
    career_values = models.TextField(help_text="Comma Seperated values")
      
      
    # Skills and Abilities
    technical_skills = models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    soft_skills = models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    other_relevant_skills =  models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    
    # Career-Related Experience
    part_time_internships =  models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    career_related_projects =  models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    career_revelant_work_experiences =  models.TextField(help_text="Comma Seperated values", blank=True, null=True)
    
    # Career Preferences and Decision-Making
    career_options =  models.TextField(help_text="Comma Seperated values")
    career_decision =  models.TextField(help_text="Comma Seperated values")
    parental_influence =  models.CharField(max_length=100)
    
    # Goals and Expectations
    short_term_career_goals = models.TextField(help_text="Comma Seperated values")
    long_term_career_goals = models.TextField(help_text="Comma Seperated values")
    career_aspirations = models.TextField(help_text="Comma Seperated values")
    
    # Social Environment and Career Values
    social_environment =  models.TextField(help_text="Comma Seperated values")
    impact_of_social_environment =  models.TextField(max_length=200)
    
    
    # Counselor's Assessment
    your_expectation = models.TextField(max_length=200)
    benifit_in_career_journey = models.TextField(max_length=200)
    questions_about_counselling_process = models.TextField(max_length=200)
    intend_to_pursue_abroad = models.TextField(max_length=200)
    previously_explored_any_career_options =  models.TextField(max_length=200)
    preferred_learning_style = models.TextField(max_length=200)
    any_believe_in_sc_and_ob_approach = models.TextField(max_length=200)
    
    # Additional Information
    additional_info = models.TextField(max_length=200) 
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    
    
    
    