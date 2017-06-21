# -*- coding: utf-8  -*-
from django import forms
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from certificates.admin import certificate_admin
from ckeditor.widgets import CKEditorWidget
from core.admin import ModelAdminReadOnly
from core.forms import OptionalForm
from core.utils import BASIC_SEARCH_FIELDS
from . import models


def mark_deleted(modeladmin, request, queryset):
    queryset.update(is_deleted=True)
mark_deleted.short_description = u"علم السجلات المُحدّدة أنها محذوفة (دون إزالتها من قاعدة البيانات)"

class AbstractFigureInline(admin.TabularInline):
    model = models.AbstractFigure
    form = OptionalForm
    extra = 0

class QuestionInline(admin.TabularInline):
    model = models.Question
    extra = 1
    
class InitiativeFigureInline(admin.TabularInline):
    model = models.InitiativeFigure
    extra = 0


class RegistrationUniversityFilter(admin.SimpleListFilter):
    title = "University"
    parameter_name = 'university'
    def lookups(self, request, model_admin):
        return (
            ('ksauhs', 'KSAU-HS'),
            ('other', 'Others')
            )

    def queryset(self, request, queryset):
        if self.value() == 'ksauhs':
            return queryset.filter(user__isnull=False)
        elif self.value() == 'other':
            return queryset.filter(nonuser__isnull=False)

class EventFilter(admin.SimpleListFilter):
    title = "Event"
    parameter_name = 'event'
    def lookups(self, request, model_admin):
        return models.Event.objects.values_list('pk', 'name') 

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(first_priority_sessions__event__pk=self.value()).distinct()

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['pk', '__unicode__', 'get_university', 'get_college',
                    'date_submitted']
    list_filter = [RegistrationUniversityFilter, EventFilter]
    search_fields = BASIC_SEARCH_FIELDS + ['nonuser__email',
                                           'nonuser__mobile_number',
                                           'nonuser__en_first_name',
                                           'nonuser__en_middle_name',
                                           'nonuser__en_last_name',
                                           'nonuser__ar_first_name',
                                           'nonuser__ar_middle_name',
                                           'nonuser__ar_last_name']

class RegistrationInline(admin.StackedInline):
    model = models.Registration
    extra = 1
    max_num = 1
    fields = ['sessions']
    
class NonUserAdmin(admin.ModelAdmin):
    list_display = ['pk', '__unicode__', 'university', 'college',
                    'with_deleted_registration', 'date_submitted']
    search_fields= ('email',
                    'en_first_name',
                    'en_middle_name',
                    'en_last_name',
                    'ar_first_name',
                    'ar_middle_name',
                    'ar_last_name')

    def with_deleted_registration(self, obj):
        return obj.hpc2016_registration.is_deleted
    with_deleted_registration.boolean = True

    inlines = [RegistrationInline]

class AbstractPosterInline(admin.TabularInline):
     model= models.AbstractPoster
     form = OptionalForm
     extra = 0

class SurveyQuestionInline(admin.TabularInline):
    model= models.SurveyQuestion

class SurveyAnswerInline(admin.TabularInline):
    model= models.SurveyAnswer
    exclude = ['text_value', 'numerical_value']
    readonly_fields = ['question', 'get_value']

class AbstractAdmin(admin.ModelAdmin):
    search_fields = BASIC_SEARCH_FIELDS + ["email", "title"]
    actions = [mark_deleted]
    list_filter = ["event", "is_deleted"]
    readonly_fields = ['user']
    inlines = [AbstractFigureInline,AbstractPosterInline]
    filter_horizontal = ('evaluators',)
    introduction = forms.CharField(widget=CKEditorWidget())

class InitiativeAdmin(admin.ModelAdmin):
    inlines = [InitiativeFigureInline]
    actions = [mark_deleted]

class SessionGroupAdmin(admin.ModelAdmin):
    list_filter = ['event']
    list_display = ['title', 'event']

class AttendanceAdmin(admin.ModelAdmin):
    list_filter = ['session_registration__session__event', 'category', 'is_deleted']
    list_display = ['__unicode__', 'category', 'date_submitted', 'is_deleted']
    readonly_fields = ['session_registration', 'submitter']
    actions = [mark_deleted]
    search_fields = ['session_registration__' + field
                     for field in BASIC_SEARCH_FIELDS]

class EventAdmin(admin.ModelAdmin):
    list_display = search_fields = ['official_name', 'english_name',
                                    'code_name']

class SessionAdmin(admin.ModelAdmin):
    list_filter = ['event']
    list_display = ['name', 'event', 'date', 'start_time', 'end_time',
                    'limit', 'get_registration_count']
    search_fields = ['name', 'event__official_name',
                     'event__english_name']

class SessionRegistrationAdmin(admin.ModelAdmin):
    readonly_fields = ['user']
    actions = [mark_deleted]
    list_display = ['__unicode__',  'is_approved', 'is_deleted',
                    'date_submitted']
    search_fields = BASIC_SEARCH_FIELDS + ['session__name']
    list_filter = ['session__event', 'is_deleted', 'is_approved']

class QustionSessionAdmin(admin.ModelAdmin):
    search_fields = ['title', 'question__question_text']
    list_filter = ['event']
    inlines = [QuestionInline]

class SurveyAdmin(admin.ModelAdmin):
    search_fields = ['name', 'mandatory_sessions__event__official_name',
                     'optional_sessions__event__official_name']
    list_filter = ['mandatory_sessions__event',
                   'optional_sessions__event']
    list_display = ['__unicode__', 'get_response_count']
    inlines = [SurveyQuestionInline]

class SurveyResponseAdmin(ModelAdminReadOnly, admin.ModelAdmin):
    search_fields = ['survey__name'] + BASIC_SEARCH_FIELDS
    list_filter = ['survey', 'session__event']
    fields = []
    inlines = [SurveyAnswerInline]

admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Session, SessionAdmin)
admin.site.register(models.CaseReport)
admin.site.register(models.Registration, RegistrationAdmin)
admin.site.register(models.NonUser, NonUserAdmin)
admin.site.register(models.Abstract, AbstractAdmin)
admin.site.register(models.TimeSlot)
admin.site.register(models.SessionGroup, SessionGroupAdmin)
admin.site.register(models.SessionRegistration, SessionRegistrationAdmin)
admin.site.register(models.Initiative, InitiativeAdmin)
admin.site.register(models.Criterion)
admin.site.register(models.Evaluation)
admin.site.register(models.Attendance, AttendanceAdmin)
admin.site.register(models.QuestionSession, QustionSessionAdmin)
admin.site.register(models.Survey, SurveyAdmin)
admin.site.register(models.SurveyResponse, SurveyResponseAdmin)
certificate_admin.register(models.Survey, SurveyAdmin)
certificate_admin.register(models.SurveyResponse, SurveyResponseAdmin)
