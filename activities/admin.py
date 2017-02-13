# -*- coding: utf-8  -*-
from django import forms
from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from datetime import timedelta
from django.utils import timezone
from django.forms import ModelForm
from django.contrib import admin
from activities.models import Activity, Episode, Category, Evaluation, Review, Assessment, Criterion, DepositoryItem, Invitation
from clubs.models import Club
from core.models import StudentClubYear
import media.utils

class InvitationAuthenticationForm(AdminAuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active and \
           not media.utils.is_media_coordinator_or_member(user):
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
                )

class InvitationAdminSite(admin.sites.AdminSite):
    login_form = InvitationAuthenticationForm

    def has_permission(self, request):
        return media.utils.is_media_coordinator_or_member(request.user) or \
               request.user.is_superuser

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 0

class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0

class SubmissionFilter(admin.SimpleListFilter):
    title = u"تاريخ الإرسال"
    parameter_name = 'submitted'
    def lookups(self, request, model_admin):
        return (
            ('d', u'خلال يوم واحد'),
            ('w', u'خلال أسبوع واحد'),
            ('m', u'خلال شهر واحد'),
            )
    def queryset(self, request, queryset):
        if self.value():
            if self.value() == 'd':
                time_ago = timezone.now() - timedelta(days=1)
            elif self.value() == 'w':
                time_ago = timezone.now() - timedelta(days=7)
            elif self.value() == 'm':
                time_ago = timezone.now() - timedelta(days=30)
            else: # Just in case
                time_ago = timezone.now()
            return queryset.filter(submission_date__gte=time_ago)

class StatusFilter(admin.SimpleListFilter):
    title = u"الحالة"
    parameter_name = 'status'
    def lookups(self, request, model_admin):
        return (
            ('a', u'مقبول'),
            ('r', u'مرفوض'),
            ('p', u'معلق'),
            )

    def queryset(self, request, queryset):
        if self.value() == 'a':
            return queryset.filter(is_approved=True)
        elif self.value() == 'r':
            return queryset.filter(is_approved=False)
        elif self.value() == 'p':
            return queryset.filter(is_approved=None)

class ActivityAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ActivityAdminForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            year = self.instance.primary_club.year
        else:
            year = StudentClubYear.objects.current_year()
        self.fields['primary_club'].queryset = Club.objects.filter(year=year)
        self.fields['assignee'].queryset = Club.objects.filter(year=year)
        self.fields['secondary_clubs'].queryset = Club.objects.filter(year=year)
        self.fields['chosen_reviewer_club'].queryset = Club.objects.filter(year=year)

    class Meta:
        model = Activity
        fields = '__all__'

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_club', 'category',
                    'submission_date', 'is_approved',
                    'get_approval_status_message', 'get_relevance_score_average',
                    'get_quality_score_average', 'get_evaluation_count')
    list_filter = ['category', 'primary_club__city', 'gender', 'primary_club__year', SubmissionFilter, StatusFilter]
    readonly_fields = ('get_relevance_score_average', 'get_quality_score_average', )
    search_fields = ["name", "primary_club__name", ]
    filter_horizontal = ('secondary_clubs',)
    form = ActivityAdminForm
    inlines = [EpisodeInline, ReviewInline]

class EvaluationAdmin(admin.ModelAdmin):
    readonly_fields = ('relevance', 'quality')
    list_display = ('episode', 'evaluator', 'relevance', 'quality')

class DepositoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit')

class InvitationAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InvitationAdminForm, self).__init__(*args, **kwargs)
        self.fields['club'].queryset = Club.objects.current_year()

    class Meta:
        model = Invitation
        fields = '__all__'

class InvitationAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_start_datetime',
                    'get_student_count', 'submission_date')
    search_fields = ('title',)
    readonly_fields = ['activity']
    filter_horizontal = ('students',)
    readonly_fields = ('students', 'get_attendees')
    form = InvitationAdminForm

    def get_attendees(self, instance):
        female_attendees = instance.students.filter(common_profile__college__gender="F")
        male_attendees = instance.students.filter(common_profile__college__gender="M")
        female_html = u"<strong>طالبات</strong><ol>\n" + format_html_join(
            '\n',
            u'<li>{}</li>',
            ((student.common_profile.get_ar_full_name(),) for student in female_attendees),
        ) + u"\n</ol>"
        male_html = u"<strong>طلاب</strong>\n<ol>\n" + format_html_join(
            '\n',
            u'<li>{}</li>',
            ((student.common_profile.get_ar_full_name(),) for student in male_attendees),
        ) + u"\n</ol>"
        return u"<br>" + female_html + male_html

    get_attendees.allow_tags = True

    
    def get_student_count(self, obj):
        return obj.students.count()

    def has_module_permission(self, request, obj=None):
        return media.utils.is_media_coordinator_or_member(request.user) or \
               request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return media.utils.is_media_coordinator_or_member(request.user) or \
               request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return media.utils.is_media_coordinator_or_member(request.user) or \
               request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return media.utils.is_media_coordinator_or_member(request.user) or \
               request.user.is_superuser


class CriterionAdmin(admin.ModelAdmin):
    list_filter = ['year', 'category']

invitation_admin = InvitationAdminSite("Invitation Admin")
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Category)
admin.site.register(Assessment)
admin.site.register(Criterion, CriterionAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(DepositoryItem, DepositoryItemAdmin)
admin.site.register(Invitation, InvitationAdmin)
invitation_admin.register(Invitation, InvitationAdmin)
