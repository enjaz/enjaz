from django.contrib import admin
from questions.models import Choice,Question,QuestionFigure,Booth

class ChoiceInline (admin.TabularInline):
    model= Choice
    extra=0

class QuestionFigureInline (admin.TabularInline):
    model = QuestionFigure
    extra =0

class QuestionAdmin (admin.ModelAdmin):

    inlines=[ChoiceInline,QuestionFigureInline ]



admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Booth)
admin.site.register(QuestionFigure)


# Register your models here.
