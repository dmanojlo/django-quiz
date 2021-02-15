from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F #F() expressions are good for memory
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.db import transaction

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import QuizName, Question, Answer
from .forms import QuizNameForm, QuestionForm, AnswerForm
# Create your views here.

class QuizListView(ListView):
    model = QuizName
    context_object_name = 'quiz_list'
    template_name = 'quiz/list_quizes.html'

    def get_queryset(self):
        # we use related_name from models QuizName(field user related_name = quiz) to link the user
        queryset = self.request.user.quiz.all()
        return queryset

class AnswerListView(ListView):
    model = Answer
    context_object_name = 'answers'
    template_name = 'quiz/answers_list.html'
    def get_queryset(self, *args, **kwargs):
        return Answer.objects.filter(question__id=self.kwargs['pk']) # self.kwargs['pk'] gets the pk passed from the url

class AnswerUpdateView(UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'quiz/answers.html'
    def get_success_url(self):
        return reverse('quiz:quiz_list')

class QuizNameCreateView(CreateView):
    model = QuizName
    template_name = 'quiz/home.html'
    form_class = QuizNameForm

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.user = self.request.user #connecting table with the user
        quiz.save()
        messages.success(self.request, 'Quiz was created with succes! Go make some question.')
        return redirect('quiz:add_question', quiz.pk)



class QuizUpdateView(UpdateView):
    model = QuizName
    fields = ['name']
    context_object_name = 'quiz'
    template_name = 'quiz/change_quizes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # we use related_name from models Question(quiz field has related_name = questions)
        # to link the questions with quizname
        context['questions'] = self.get_object().questions.all()
        return context

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.quiz.all()


# class QuestionsCreateView(CreateView):
#     model = Question
#     template_name = 'quiz/questions.html'
#     form_class = QuestionForm
#
#     def form_valid(self, form):
#         return super().form_valid(form)

def add_question(request, pk):
    quiz = get_object_or_404(QuizName, pk=pk, user = request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'You may add answers!')
            return redirect('quiz:question_answers', quiz.pk, question.pk)
    else:
        form = QuestionForm()
    return render(request, 'quiz/questions.html',  {'quiz': quiz, 'form': form})


def question_answers(request, quiz_pk, question_pk):
    quiz = get_object_or_404(QuizName, pk=quiz_pk, user = request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz = quiz)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        fields=('text', 'is_correct'),
        min_num=2,
        extra = 1,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            # answer = form.save(commit=False)
            # answer.question = question #for connecting tables with foreign key
            # answer.save()
            messages.success(request, 'Answers saved with success!')
            return redirect('quiz:quiz_name')
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)
    return render(request, 'quiz/answers_list.html', {'form':form, 'formset': formset, 'quiz':quiz, 'question':question})
