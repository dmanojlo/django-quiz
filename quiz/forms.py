from django import forms
from django.forms import ModelForm
from .models import QuizName, Question, Answer

class QuizNameForm(forms.ModelForm):

    class Meta:
        model = QuizName
        fields = ['name']


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['text']

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['text', 'is_correct']
