from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required #for function based views
from django.contrib.auth.mixins import LoginRequiredMixin #for classed based views
from django.db.models import F #F() expressions are good for memory
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.db import transaction
from django.core.cache import cache

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import QuizName, Question, Answer
from .forms import QuizNameForm, QuestionForm, AnswerForm, TakeQuizForm, BaseAnswerInlineFormset
# Create your views here.

import json

class QuizChooseView(ListView):
    model = QuizName
    template_name = 'quiz/choose_quiz.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # we use related_name from models Question(quiz field has related_name = questions)
        # to link the questions with quizname
        quiz_name = QuizName.objects.values_list('name', flat=True)
        quiz_pk = QuizName.objects.values_list('pk', flat=True)
        question_pk = []
        for i in quiz_pk:
            question_pk.append(Question.objects.filter(quiz=i).values_list('pk', flat=True)[0])
        myziped = zip(quiz_name, quiz_pk, question_pk)
        context['questions'] = myziped
        return context


class QuizListView(LoginRequiredMixin,ListView):
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

class QuizStartView(ListView):
    model = QuizName
    template_name = 'quiz/start_quiz.html'

class QuizNameIndexView(CreateView):
    model = QuizName
    template_name = 'quiz/index.html'
    form_class = QuizNameForm

class QuizNameCreateView(LoginRequiredMixin,CreateView):
    model = QuizName
    template_name = 'quiz/create_quiz.html'
    form_class = QuizNameForm

    def form_valid(self, form):
        data = dict()
        quiz = form.save(commit=False)
        quiz.user = self.request.user #connecting table with the user
        quiz.save()
        messages.success(self.request, 'Quiz was created with succes! Go make some question.')
        #return redirect('quiz:add_question', quiz.pk)
        data['url'] = reverse('quiz:add_question', args=[quiz.pk]) #redirect to next question
        return JsonResponse(data)

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

    def get_success_url(self):
        messages.success(self.request, 'Quiz name was changed with succes! Go make some questions.')
        return self.request.path

class QuizDeleteView(DeleteView):
    model = QuizName
    context_object_name = 'quiz'
    template_name = 'quiz/quiz_delete.html'


    def get_success_url(self):
        #to get data from Question model you have to use self.get_object()
        quiz = self.get_object()
        return reverse('quiz:quiz_list')


class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'quiz/question_delete.html'


    def get_success_url(self):
        #to get data from Question model you have to use self.get_object()
        question = self.get_object()
        return reverse('quiz:quiz_update', kwargs={'pk': question.quiz.pk})

# class QuestionsCreateView(CreateView):
#     model = Question
#     template_name = 'quiz/questions.html'
#     form_class = QuestionForm
#
#     def form_valid(self, form):
#         return super().form_valid(form)



def add_question(request, pk):
    data = dict()
    quiz = get_object_or_404(QuizName, pk=pk, user = request.user)
    #previous_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            data['urlans'] = reverse('quiz:question_answers', args=[quiz.pk, question.pk]) #redirect to next question
            return JsonResponse(data)
            #return redirect('quiz:question_answers', quiz.pk, question.pk)
    else:
        form = QuestionForm()
    return render(request, 'quiz/questions.html',  {'quiz': quiz, 'form': form})



def question_answers(request, quiz_pk, question_pk):
    quiz = get_object_or_404(QuizName, pk=quiz_pk, user = request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz = quiz)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset = BaseAnswerInlineFormset,
        fields=('text', 'is_correct'),
        min_num=2,
        extra = 2,
        validate_min=True,
        max_num=4,
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
            # data['urli'] = reverse('quiz:question_answers', args=[quiz.pk, question.pk]) #redirect to next question
            # print(data)
            # return JsonResponse(data)
            return redirect('quiz:quiz_update', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)
    return render(request, 'quiz/answers_list.html', {'form':form, 'formset': formset, 'quiz':quiz, 'question':question})

#--------------------


def start_quiz(request, quiz_pk, question_pk):
    data = dict()
    quiz = get_object_or_404(QuizName, pk=quiz_pk)
    question = get_object_or_404(Question, pk=question_pk, quiz = quiz)
    next_question = Question.objects.filter(quiz=quiz, id__gt=question_pk).order_by('id').first()
    correct_answer = Answer.objects.get(question=question, is_correct=True)
    number_of_questions = Question.objects.filter(quiz=quiz_pk).count()
    if request.method == 'POST':
        form = TakeQuizForm(request.POST, question=question)
        if form.is_valid():
            # if correct_answer == form.cleaned_data['answer']:
            #     score += 1
            if next_question != None:
                data['form_is_valid'] = True
                #data['html_form'] = render_to_string('quiz/partial_radio.html', {'qui':14, 'ques':next_question.id, 'quiz':quiz, 'form':form, 'question':question, 'correct_answer': correct_answer}, request=request)
                data['url'] = reverse('quiz:start_quiz', args=[quiz.pk, next_question.id]) #redirect to next question
                return JsonResponse(data)
            else:
                data['form_is_valid'] = False
                # if score < (number_of_questions//2):
                #     data['message'] = 'As expected. You are an idiot. Your miserable score is ' + str(score) + '/' + str(number_of_questions)
                # else:
                #     data['message'] = 'Unbelivable. Your little brain got ' + str(score) + '/' + str(number_of_questions)
                # score = 0
                return JsonResponse(data)


    else:
        form = TakeQuizForm(question=question)

    return render(request, 'quiz/start_quiz.html', {'quiz':quiz, 'form':form, 'question':question, 'correct_answer': correct_answer, 'num_of_q':number_of_questions})


#web: gunicorn django_quiz.wsgi --log-file -
