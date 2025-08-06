from django.db import models #type:ignore

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    class UserGroup(models.TextChoices):
        CLASS_8_10 = 'class_8_10', 'Class 8-10'
        CLASS_11_12 = 'class_11_12', 'Class 11-12'
        COLLEGE = 'college', 'College Students'
        WORKING = 'working', 'Working Professionals'

    class QuestionType(models.TextChoices):
        MCQ = 'mcq', 'Multiple Choice'
        TRUE_FALSE = 'true_false', 'True/False'
        SHORT_ANSWER = 'short', 'Short Answer'
        MATCHING = 'matching', 'Matching'
        FILL_BLANK = 'fill_blank', 'Fill in the Blank'

    question_text = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="questions")
    user_group = models.CharField(max_length=20, choices=UserGroup.choices)
    question_type = models.CharField(max_length=20, choices=QuestionType.choices, default=QuestionType.MCQ)
    explanation = models.TextField(blank=True, null=True)
    correct_answer = models.TextField(blank=True, null=True)
    true_false_answer = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True )
    
    def __str__(self):
        return f"{self.get_user_group_display()} - Q{self.id}"

    def save(self, *args, **kwargs):
        # Clear unnecessary correct answer fields based on question type
        if self.question_type != Question.QuestionType.TRUE_FALSE:
            self.true_false_answer = None
        if self.question_type not in [Question.QuestionType.SHORT_ANSWER, Question.QuestionType.FILL_BLANK]:
            self.correct_answer = None
        super().save(*args, **kwargs)

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    label = models.CharField(max_length=1, choices=[(chr(i), chr(i)) for i in range(65, 91)])  # A-Z
    text = models.TextField(blank=True, null=True)
    match_text = models.TextField(blank=True, null=True)  # For matching questions
    image = models.ImageField(upload_to='option_images/', blank=True, null=True)
    is_correct = models.BooleanField(default=False)  # For MCQ and matching questions

    class Meta:
        unique_together = ('question', 'label')

    def __str__(self):
        return f"Q{self.question.id} - {self.label}"