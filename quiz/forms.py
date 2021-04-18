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


class BaseAnswerInlineFormset(forms.BaseInlineFormSet):

    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if form.cleaned_data.get('is_correct', False):
                has_one_correct_answer = True
                break
        if not has_one_correct_answer:
            raise forms.ValidationError('Mark at least one answer as correct.', code='no_correct_answer')

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
