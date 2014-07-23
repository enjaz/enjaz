# -*- coding: utf-8  -*-
from django import forms

from django.contrib import admin
from django.contrib.auth import authenticate
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ObjectDoesNotExist

from arshidni.models import Question, Answer, StudyGroup, LearningObjective, group_status_choices, ColleagueProfile, GraduateProfile

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

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'submitter', 'is_answered',
                    'is_published', 'submission_date')
    list_filter = [PublishedFilter]
    inlines = [AnswerInline]

class ColleagueProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'batch',)

class GraduateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'answers_questions', 'gives_lectures')


arshidni_admin = ArshidniAdmin("Arshidni Admin")

admin.site.register(StudyGroup, StudyGroupAdmin)
arshidni_admin.register(StudyGroup, StudyGroupAdmin)

admin.site.register(Question, QuestionAdmin)
arshidni_admin.register(Question, QuestionAdmin)

admin.site.register(ColleagueProfile, ColleagueProfileAdmin)
arshidni_admin.register(ColleagueProfile, ColleagueProfileAdmin)


admin.site.register(GraduateProfile, GraduateProfileAdmin)
arshidni_admin.register(GraduateProfile, GraduateProfileAdmin)
