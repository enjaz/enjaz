from django.contrib import admin
from questions.models import Game, Choice, Question, QuestionFigure, Booth

class ChoiceInline(admin.TabularInline):
    model= Choice
    extra=0

class QuestionFigureInline(admin.TabularInline):
    model = QuestionFigure
    extra =0

class QuestionAdmin(admin.ModelAdmin):
    inlines=[ChoiceInline, QuestionFigureInline]
    list_display = ['text', 'question_type', 'booth']
    list_filter = ['question_type', 'booth']

class GameAdmin(admin.ModelAdmin):
    list_display = ['user', 'right_answers', 'submission_date']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Booth)
admin.site.register(Game, GameAdmin)
