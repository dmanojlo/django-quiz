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

class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(queryset=Answer.objects.none(),
                                    widget=forms.RadioSelect(),
                                    required=True,
                                    empty_label=None
                                    )
    class Meta:
        model = Answer
        exclude = ('text', 'question', 'is_correct',)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')
