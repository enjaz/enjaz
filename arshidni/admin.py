# -*- coding: utf-8  -*-
from django import forms

from django.contrib import admin
from django.contrib.auth import authenticate
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ObjectDoesNotExist

from arshidni.models import Question, Answer, StudyGroup, LearningObjective, JoinStudyGroupRequest, group_status_choices, ColleagueProfile, SupervisionRequest, GraduateProfile, supervision_request_status_choices

class ArshidniAuthenticationForm(admin.forms.AdminAuthenticationForm):
    """A custom authentication form used in the admin app.  Based on the
original Django code."""
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = admin.forms.ERROR_MESSAGE
        params = {'username': self.username_field.verbose_name}
        arshidni_group = Group.objects.get(name='arshidni')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(message, code='invalid', params=params)
            # If the user isn't in the arshidni group and isn't a
            # system administrator, they must not be able to use the
            # arshidni admin interface.
            elif not arshidni_group in self.user_cache.groups.all() and\
                 not self.user_cache.is_superuser:
                raise forms.ValidationError(message, code='invalid', params=params)
        return self.cleaned_data

class ArshidniAdmin(AdminSite):
    """This admin website is for the coordinator of Arshidni program
so they can monitor the different aspects of the section."""

    login_form = ArshidniAuthenticationForm

    def has_permission(self, request):
        arshidni_group = Group.objects.get(name='arshidni')
        return arshidni_group in request.user.groups.all() or request.user.is_superuser

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1

class LearningObjectiveInline(admin.StackedInline):
    model = LearningObjective
    extra = 1

# TODO: actions to approve and reject study groups.

class GroupStatusFilter(admin.SimpleListFilter):
    title = u"حالة المجموعة"
    parameter_name = 'group_status'
    def lookups(self, request, model_admin):
        return group_status_choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())

class SupervisionRequestStatusFilter(admin.SimpleListFilter):
    title = u"حالة الطلب"
    parameter_name = 'request_status'

    def lookups(self, request, model_admin):
        return supervision_request_status_choices
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())

class ColleagueAvailabilityFilter(admin.SimpleListFilter):
    title = u"توفر الزميل"
    parameter_name = 'available'
    def lookups(self, request, model_admin):
        return (
            (0, u'غير متوفر'),
            (1, u'متوفر'),)

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(is_available=False)
        elif self.value() == '1':
            return queryset.filter(is_available=True)

class PublishedFilter(admin.SimpleListFilter):
    title = u"النشر"
    parameter_name = 'published'
    def lookups(self, request, model_admin):
        return (
                ('P', u'لم يراجع بعد'),
                ('A', u'منشور'),
                ('R', u'محذوف'),
            )


    def queryset(self, request, queryset):
        if self.value() == 'R':
            return queryset.filter(is_published=False)
        elif self.value() == 'A':
            return queryset.filter(is_published=True)
        elif self.value() == 'P':
            return queryset.filter(is_published=None)

class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'coordinator', 'submission_date', 'starting_date',
                    'get_period_in_weeks', 'status')
    list_filter = [GroupStatusFilter]
    inlines = [LearningObjectiveInline]

class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = ('group', 'is_done', 'submission_date')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'submitter', 'is_answered',
                    'is_published', 'submission_date')
    list_filter = [PublishedFilter]
    inlines = [AnswerInline]

class ColleagueProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user_full_name', 'batch', 'is_available')
    list_filter = [ColleagueAvailabilityFilter]

    def get_user_full_name(self, obj):
        return obj.user.student_profile.get_ar_full_name()
    get_user_full_name.short_description = u"اسم الزميل الطلابي"

class GraduateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'answers_questions', 'gives_lectures')

class SupervisionRequestAdmin(admin.ModelAdmin):
    list_display = ('get_user_full_name', 'batch', 'get_colleague_full_name', 'status', 'submission_date')
    list_filter = [SupervisionRequestStatusFilter]

    def get_user_full_name(self, obj):
        return obj.user.student_profile.get_ar_full_name()
    get_user_full_name.short_description = u"اسم الطالب المستجد"

    def get_colleague_full_name(self, obj):
        return obj.colleague.user.student_profile.get_ar_full_name()
    get_colleague_full_name.short_description = u"اسم الزميل الطلابي"

class JoinStudyGroupRequestAdmin(admin.ModelAdmin):
    list_display = ('submitter', 'group', 'is_accepted', 'submission_date')

arshidni_admin = ArshidniAdmin("Arshidni Admin")

admin.site.register(StudyGroup, StudyGroupAdmin)
arshidni_admin.register(StudyGroup, StudyGroupAdmin)

admin.site.register(JoinStudyGroupRequest, JoinStudyGroupRequestAdmin)
arshidni_admin.register(JoinStudyGroupRequest, JoinStudyGroupRequestAdmin)

admin.site.register(Question, QuestionAdmin)
arshidni_admin.register(Question, QuestionAdmin)

admin.site.register(LearningObjective, LearningObjectiveAdmin)
arshidni_admin.register(LearningObjective, LearningObjectiveAdmin)

admin.site.register(ColleagueProfile, ColleagueProfileAdmin)
arshidni_admin.register(ColleagueProfile, ColleagueProfileAdmin)

admin.site.register(SupervisionRequest, SupervisionRequestAdmin)
arshidni_admin.register(SupervisionRequest, SupervisionRequestAdmin)

admin.site.register(GraduateProfile, GraduateProfileAdmin)
arshidni_admin.register(GraduateProfile, GraduateProfileAdmin)

