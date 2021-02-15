from django.contrib import admin
from .models import QuizName, Question, Answer

# Register your models here.
class AnswerTabularInline(admin.TabularInline):
    model = Answer
    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerTabularInline]
    class Meta:
        model = Question

admin.site.register(QuizName)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
