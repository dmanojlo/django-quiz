from django.urls import path, include
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from .views import ( QuizNameIndexView,
                     QuizNameCreateView,
                     QuizUpdateView,
                     QuizListView,
                     add_question,
                     question_answers,
                     AnswerListView,
                     AnswerUpdateView,
                     #take_quiz,
                     start_quiz,
                     QuizStartView,
                     QuizChooseView

                    )


app_name = 'quiz' # za url putanju do appa

urlpatterns = [
     path('list_quizes/', QuizListView.as_view(), name='quiz_list'),
     path('change_quizes/<int:pk>/', QuizUpdateView.as_view(), name='quiz_update'),
     path('index/', QuizNameIndexView.as_view(), name='quiz_name'),
     path('create_quiz/', QuizNameCreateView.as_view(), name='quiz_create'),
     path('choose_quiz/', QuizChooseView.as_view(), name='choose_quiz'),
     path('questions/<int:pk>/', add_question, name='add_question'),
     path('<int:quiz_pk>/question/<int:question_pk>/', question_answers, name='question_answers'),
     path('answers_list/<int:pk>/', AnswerListView.as_view(), name='answer_list'),
     path('answers_update/<int:pk>/', AnswerUpdateView.as_view(), name='answer_update'),
     #Students path
     #path('start_quiz/', QuizStartView.as_view(), name='start_quiz'),
     path('start_quiz/<int:quiz_pk>/question/<int:question_pk>/', start_quiz, name='start_quiz'),
     #path('take_quiz/<int:quiz_pk>/question/<int:question_pk>/', take_quiz, name='take_quiz'),
    # path('register/', register_view, name='register'),
    # path('login/', login_view, name='login'),
    # path('logout/', logout_view, name='logout'),
    # #path('item_create/', item_create_view, name='item_create_view'),
    # path('admin_panel/', item_create_view, name='item_create_view'),
    # #path('item_list/', item_list, name='item_list'),
    # path('shop_list/', item_list, name='item_list'),
    # path('decrement_quantity/<int:pk>/', decrement_quantity, name='decrement_quantity'),
    # path('delete/<int:pk>/', item_delete_view, name='item_delete_view'),
    # path('edit/<int:pk>/', item_edit_view, name='item_edit_view'),
    # # path('article_create/', ArticleCreateView.as_view(), name='article-create'),
    # # path('<int:id>/', ArticleDetailView.as_view(), name='article-detail'),
    # # path('<int:id>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
]
