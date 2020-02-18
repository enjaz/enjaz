# -*- coding: utf-8  -*-
from django.contrib import admin

from .models import Inventor, ContestQuestion, ContestAnswer, Contest


def mark_excludable(modeladmin, request, queryset):
    queryset.update(is_excludable=True)
mark_excludable.short_description = u"علّم الخيارات المُحدّدة أنها قابلة للحذف عند اختيار وسيلة المساعدة)"


class InventorAdmin(admin.ModelAdmin):
    list_filter = ['inv_category', 'is_prototype']
    list_display = ['__unicode__', 'ar_name', 'en_name', 'prototype_file', 'submission_date']
    search_fields = ['ar_name', 'en_name', 'invention_name', 'inv_category', 'summary']

class ContestQuestionAdmin (admin.ModelAdmin):
    list_filter = ['category', 'olympiad_version', 'contest']
    list_display = ['__unicode__', 'category', 'olympiad_version']
    search_fields = list_display

class ContestAnswerAdmin (admin.ModelAdmin):
    list_filter = ['question__olympiad_version']
    list_display = ['__unicode__', 'question', 'choice_letter', 'is_correct', "is_excludable"]
    search_fields = ['__unicode__', 'question', 'is_correct', 'question.olympiad_version']
    actions = [mark_excludable]

admin.site.register(Inventor, InventorAdmin)
admin.site.register(ContestQuestion, ContestQuestionAdmin)
admin.site.register(ContestAnswer, ContestAnswerAdmin)
admin.site.register(Contest)
