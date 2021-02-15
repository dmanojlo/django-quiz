from django.db import models
from django.conf import settings
# Create your models here.

class QuizName(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Question(models.Model):
    # relted_name - the name to use for the relation from the related object back to this one
    quiz = models.ForeignKey(QuizName, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
