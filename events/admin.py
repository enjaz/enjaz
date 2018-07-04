# -*- coding: utf-8  -*-
from functools import update_wrapper

import openpyxl
from django import forms
from django.conf.urls import url
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.http import urlquote
from django.utils.translation import ugettext, ugettext_lazy as _

from certificates.admin import certificate_admin, CertificateAdminPermission
from ckeditor.widgets import CKEditorWidget
from core.admin import ModelAdminReadOnly
from core.forms import OptionalForm
from core.utils import BASIC_SEARCH_FIELDS
from events.models import Survey
from . import models
import events.forms




def mark_deleted(modeladmin, request, queryset):
    queryset.update(is_deleted=True)
mark_deleted.short_description = u"علم السجلات المُحدّدة أنها محذوفة (دون إزالتها من قاعدة البيانات)"


class AuthorInline(admin.TabularInline):
    model = models.AbstractAuthor
    form = OptionalForm
    extra = 1

class AbstractFigureInline(admin.TabularInline):
    model = models.AbstractFigure
    form = OptionalForm
    extra = 0

class AbstractPosterInline(admin.TabularInline):
    model = models.AbstractPoster
    form = OptionalForm
    extra = 0

class AbstractAdmin(admin.ModelAdmin):
    search_fields = BASIC_SEARCH_FIELDS + ["email", "title"]
    actions = [mark_deleted]
    list_filter = ["event", "is_deleted"]
    list_display = ['__unicode__', 'is_deleted', 'status',
                    'date_submitted']
    inlines = [AuthorInline, AbstractFigureInline, AbstractPosterInline]
    filter_horizontal = ('evaluators',)
    raw_id_fields = ['evaluators']
    introduction = forms.CharField(widget=CKEditorWidget())


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
    search_fields = ('email',
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


class SurveyQuestionInline(admin.TabularInline):
    model = models.SurveyQuestion


class SurveyAnswerInline(CertificateAdminPermission, admin.TabularInline):
    model = models.SurveyAnswer
    exclude = ['text_value', 'numerical_value']
    readonly_fields = ['question', 'get_value']


class InitiativeAdmin(admin.ModelAdmin):
    inlines = [InitiativeFigureInline]
    actions = [mark_deleted]


class SessionGroupAdmin(admin.ModelAdmin):
    list_filter = ['event']
    list_display = ['title', 'event']


class AttendanceAdmin(admin.ModelAdmin):
    form = events.forms.AttendanceAdminForm
    list_filter = ['session_registration__session__event', 'category', 'is_deleted']
    list_display = ['__unicode__', 'category', 'date_submitted', 'is_deleted']
    readonly_fields = ['session_registration']
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
    form = events.forms.SessionRegistrationAdminForm
    actions = [mark_deleted]
    list_display = ['__unicode__', 'is_approved', 'is_deleted',
                    'date_submitted']
    search_fields = BASIC_SEARCH_FIELDS + ['session__name']
    list_filter = ['session__event', 'is_deleted', 'is_approved']


class QustionSessionAdmin(admin.ModelAdmin):
    search_fields = ['title', 'question__question_text']
    list_filter = ['event']
    inlines = [QuestionInline]


class SurveyAdmin(CertificateAdminPermission, admin.ModelAdmin):
    search_fields = ['name', 'mandatory_sessions__event__official_name',
                     'optional_sessions__event__official_name']
    list_filter = ['mandatory_sessions__event',
                   'optional_sessions__event']
    list_display = ['__unicode__', 'get_response_count', 'link_to_excel_results']
    inlines = [SurveyQuestionInline]

    def link_to_excel_results(self, obj):
        return '<a href="{}">{}</a>'.format(
            reverse("admin:events_survey_results", args=(obj.id,)),
            _(u"حمّل النتائج كملف إكسل")
        )
    link_to_excel_results.allow_tags = True
    link_to_excel_results.short_description = _(u"النتائج")

    def get_urls(self):
        urlpatterns = super(SurveyAdmin, self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(r'^(.+)/results/$', wrap(self.results_as_excel), name='%s_%s_results' % info),
        ] + urlpatterns
        return urlpatterns

    def results_as_excel(self, request, object_id, extra_context=None):
        survey = get_object_or_404(Survey, id=object_id)
        output = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; charset=utf-8'
        )
        file_name = "{} - {}.xlsx".format(survey.name.encode('utf-8'), _(u"النتائج"))
        # `urlquote` encodes Arabic (Unicode) characters into the appropriate %XX codes
        output['Content-Disposition'] = "attachment; filename={}".format(urlquote(file_name))

        wb = openpyxl.Workbook()
        ws = wb.active

        questions = survey.survey_questions.all()
        ws.append([ugettext(u"التاريخ"), ugettext(u"الوقت"), ugettext(u"المستخدم")] + [question.text for question in questions])

        responses = survey.responses.all().prefetch_related('answers__question')

        for response in responses:
            values = []
            for question in questions:
                try:
                    # `next` returns the next item in a sequence
                    # In this configuration, it's going to return the first element that matches the `if` condition
                    # This has a big performance advantage
                    # Check: https://stackoverflow.com/a/9868665
                    # and: https://stackoverflow.com/a/2364277
                    answer = next(answer for answer in response.answers.all() if answer.question == question)
                    value = answer.numerical_value if question.category == 'S' else answer.text_value
                    values.append(value)
                except StopIteration:
                    values.append("")

            ws.append(
                [response.date_submitted.strftime("%m/%d/%Y"), response.date_submitted.strftime("%H:%M:%S"), response.user.username] + values
            )

        wb.save(output)

        return output


class SurveyResponseAdmin(CertificateAdminPermission, ModelAdminReadOnly, admin.ModelAdmin):
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
