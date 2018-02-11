# -*- coding: utf-8  -*-
from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import format_html

from core.admin import ModelAdminReadOnly
from . import models, utils


class BulbAuthenticationForm(AdminAuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active and \
            not (utils.is_bulb_coordinator_or_deputy(user) or \
                         utils.is_bulb_member(user)):
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
                )


class BulbAdmin(admin.sites.AdminSite):
    login_form = BulbAuthenticationForm

    def has_permission(self, request):
        return utils.is_bulb_coordinator_or_deputy(request.user) or \
           utils.is_bulb_member(request.user) or \
           request.user.is_superuser


class BookRecommendationInline(admin.TabularInline):
    model = models.BookRecommendation
    extra = 1
    readonly_fields = ['user']


class MembershipInline(admin.TabularInline):
    model = models.Membership
    extra = 0
    readonly_fields = ['get_name']

    def get_name(self, obj):
        try:
            return obj.user.common_profile.get_ar_full_name()
        except AttributeError:
            return obj.user.username

    get_name.short_description = "Name"


class BookAdmin(admin.ModelAdmin):
    search_fields = ['title', 'submitter__common_profile__en_first_name',
                    'submitter__common_profile__en_middle_name',
                    'submitter__common_profile__en_last_name',
                    'submitter__common_profile__ar_first_name',
                    'submitter__common_profile__ar_middle_name',
                    'submitter__common_profile__ar_last_name']

    list_display = ['title', 'submitter', 'category', 'is_available',
                    'submission_date']


class NeededBookAdmin(admin.ModelAdmin):
    search_fields = ['title', 'requester__common_profile__en_first_name',
                    'requester__common_profile__en_middle_name',
                    'requester__common_profile__en_last_name',
                    'requester__common_profile__ar_first_name',
                    'requester__common_profile__ar_middle_name',
                    'requester__common_profile__ar_last_name']

    list_display = ['title', 'requester', 'category',
                    'submission_date']

class GroupAdmin(admin.ModelAdmin):
    list_filter = ["is_deleted", ]
    inlines = [MembershipInline, ]

class BulbModelAdmin(admin.ModelAdmin):
    def get_full_ar_name(self, obj):
        try:
            return obj.user.common_profile.get_ar_full_name()
        except ObjectDoesNotExist:
            return obj.user.username

    get_full_ar_name.short_description = u"الاسم الكامل"

    def get_email(self, obj):
        return format_html("<a href=\"mailto:{0}\">{0}</a>", obj.user.email)

    get_email.short_description = u"البريد الإلكتروني"

    def get_mobile_number(self, obj):
        try:
            return obj.user.common_profile.mobile_number
        except ObjectDoesNotExist:
            return

    get_mobile_number.short_description = u"رقم الجوال"

    def get_college(self, obj):
        try:
            return obj.user.common_profile.college.get_name_display()
        except (ObjectDoesNotExist, AttributeError):
            return

    get_college.short_description = u"الكلية"

    def has_module_permission(self, request, obj=None):
        return utils.is_bulb_coordinator_or_deputy(request.user) or \
               utils.is_bulb_member(request.user) or \
               request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return utils.is_bulb_coordinator_or_deputy(request.user) or \
               utils.is_bulb_member(request.user) or \
               request.user.is_superuser

class RecruitmentAdmin(BulbModelAdmin):
    list_display = ['get_full_ar_name', 'get_email',
                    'get_mobile_number', 'get_college',
                    'prefers_coordination', 'prefers_team_membership',
                    'wants_book_exchange_organization',
                    'wants_dewanya_organization',
                    'wants_readathon_organization', 'submission_date']
    list_filter = ['year']

class RecruitmentAdminReadOnly(ModelAdminReadOnly, RecruitmentAdmin):
    pass

class SessionAdmin(admin.ModelAdmin):
    search_fields = ['title', 'group__name',
                     'submitter__common_profile__en_first_name',
                     'submitter__common_profile__en_middle_name',
                     'submitter__common_profile__en_last_name',
                     'submitter__common_profile__ar_first_name',
                     'submitter__common_profile__ar_middle_name',
                     'submitter__common_profile__ar_last_name']

    list_filter = ['submitter__common_profile__city', 'group']

    list_display = ['title', 'submitter', 'submission_date']

class BookCommitmentAdmin(BulbModelAdmin):
    search_fields = ['title', 'reason',
                     'user__common_profile__en_first_name',
                     'user__common_profile__en_middle_name',
                     'user__common_profile__en_last_name',
                     'user__common_profile__ar_first_name',
                     'user__common_profile__ar_middle_name',
                     'user__common_profile__ar_last_name']
    list_filter = ['user__common_profile__city', 'wants_to_attend']
    list_display = ['title', 'wants_to_attend',
                    'get_full_ar_name', 'get_email',
                    'get_mobile_number', 'get_college',
                    'submission_date']

class BookCommitmentAdminReadOnly(ModelAdminReadOnly, BookCommitmentAdmin):
    pass

class ReadathonAdmin(BulbModelAdmin):
    search_fields = ['publication_date', 'start_date',
                     'submission_date']
    list_filter = ['publication_date']
    list_display = ['publication_date', 'start_date',
                    'end_date', 'submission_date',
                    'template_name']

class ReadathonAdminReadOnly(ModelAdminReadOnly, ReadathonAdmin):
    pass

class RecommendedBookAdmin(admin.ModelAdmin):
    search_fields = ['title', 'authors']
    list_display = ['title', 'category', 'get_recommendation_count']
    list_filter = ['category']
    inlines = [BookRecommendationInline]

    def get_recommendation_count(self, obj):
        return obj.bookrecommendation_set.count()

class RecommendedBookAdminReadOnly(ModelAdminReadOnly, RecommendedBookAdmin):
    pass

bulb_admin = BulbAdmin("Bulb Admin")
admin.site.register(models.Category)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.NeededBook, NeededBookAdmin)
admin.site.register(models.Request)
admin.site.register(models.Point)
admin.site.register(models.Recruitment, RecruitmentAdmin)
bulb_admin.register(models.Recruitment, RecruitmentAdminReadOnly)
admin.site.register(models.NewspaperSignup)
bulb_admin.register(models.NewspaperSignup)
admin.site.register(models.Session, SessionAdmin)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.BookCommitment, BookCommitmentAdmin)
bulb_admin.register(models.BookCommitment, BookCommitmentAdminReadOnly)`
admin.site.register(models.Readathon, ReadathonAdmin)
bulb_admin.register(models.Readathon, ReadathonAdminReadOnly)
admin.site.register(models.RecommendedBook, RecommendedBookAdmin)
bulb_admin.register(models.RecommendedBook, RecommendedBookAdminReadOnly)
