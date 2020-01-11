from django.contrib import admin

from .models import Inventor, ContestQuestion, ContestAnswer

class InventorAdmin(admin.ModelAdmin):
    list_filter = ['inv_category', 'is_prototype']
    list_display = ['__unicode__', 'ar_name', 'en_name', 'prototype_file', 'submission_date']
    search_fields = ['ar_name', 'en_name', 'invention_name', 'inv_category', 'summary']

class ContestQuestionAdmin (admin.ModelAdmin):
    list_filter = ['category', 'olympiad_version']
    list_display = ['__unicode__', 'category', 'olympiad_version']
    search_fields = list_display

class ContestAnswerAdmin (admin.ModelAdmin):
    list_filter = ['question__olympiad_version']
    list_display = ['__unicode__', 'question', 'is_correct']
    search_fields = ['__unicode__', 'question', 'is_correct', 'question.olympiad_version']

admin.site.register(Inventor, InventorAdmin)
admin.site.register(ContestQuestion, ContestQuestionAdmin)
admin.site.register(ContestAnswer, ContestAnswerAdmin)
