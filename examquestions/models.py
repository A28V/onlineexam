from django.db import models
from users.models import UsersConfig

class Question(models.Model):
    OPTION_CHOICES = (
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
        ('option4', 'Option 4'),
    )
    text = models.TextField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100, choices=OPTION_CHOICES)
    difficulty_level = models.CharField(max_length=20)

class ExamName(models.Model):
    title = models.CharField(max_length=200)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    questions = models.ManyToManyField(Question)

class ExamTemplate(models.Model):
    title = models.CharField(max_length=200)
    questions = models.ManyToManyField(Question)

class Result(models.Model):
    user = models.ForeignKey(UsersConfig, on_delete=models.CASCADE)
    exam = models.ForeignKey(ExamName, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    

class Start_exam_user(models.Model):
    user = models.ForeignKey(UsersConfig, on_delete=models.CASCADE)
    exam = models.ForeignKey(ExamName, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)

class AttemptedQuestion(models.Model):
    user = models.ForeignKey(UsersConfig, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_option = models.CharField(max_length=100, help_text="Option chosen by the user")
    is_correct = models.BooleanField(default=False, help_text="Was the attempt correct?")
    exam = models.ForeignKey(ExamName, on_delete=models.CASCADE)  # Changed from exam_id
    
