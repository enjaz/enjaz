# -*- coding: utf-8  -*-
from django import forms

from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission, Group
from django.core.exceptions import ObjectDoesNotExist
from userena.admin import UserenaAdmin

from . import utils
from clubs.models import Club, college_choices, section_choices
from accounts.models import CommonProfile
from core.models import StudentClubYear
import media.utils
import clubs.utils

class UserListAuthenticationForm(AdminAuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active and \
           not (media.utils.is_media_coordinator_or_deputy(user) or \
                clubs.utils.is_presidency_coordinator_or_deputy(user)):
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
                )

class UserListAdmin(admin.sites.AdminSite):
    login_form = UserListAuthenticationForm

    def has_permission(self, request):
        return media.utils.is_media_coordinator_or_deputy(request.user) or \
               clubs.utils.is_presidency_coordinator_or_deputy(request.user) or \
               request.user.is_superuser

class CommonProfileInline(admin.StackedInline):
    model = CommonProfile
    max_num = 1
    extra = 0

def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)
make_active.short_description = u"نشّط حسابات المستخدمين والمستخدمات"


class EmployeeFilter(admin.SimpleListFilter):
    title = u"عمادة شؤون الطلاب"
    parameter_name = 'is_employee'
    def lookups(self, request, model_admin):
        return (
            ('1', u'موظف'),
            ('0', u'ليس موظف'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(user_permissions__codename='deanship_employee')
        if self.value() == '0':
            return queryset.exclude(user_permissions__codename='deanship_employee')

class CoordinatorFilter(admin.SimpleListFilter):
    title = u"تنسيق الأندية"
    parameter_name = 'is_coordinator'
    def lookups(self, request, model_admin):
        return (
            ('1', u'منسق'),
            ('0', u'ليس منسق'),
        )

    def queryset(self, request, queryset):
        current_year = StudentClubYear.objects.get_current()
        if self.value() == '1':
            return queryset.filter(coordination__year=current_year)
        if self.value() == '0':
            return queryset.exclude(coordination__year=current_year)

class CollegeFilter(admin.SimpleListFilter):
    title = u"كلية الطالب"
    parameter_name = 'college'
    def lookups(self, request, model_admin):
        return college_choices

    def queryset(self, request, queryset):
        # If the filter is actually selected, apply it
        if self.value():
            return queryset.filter(common_profile__college__name=self.value())

class SectionFilter(admin.SimpleListFilter):
    title = u"قسم الطالب"
    parameter_name = 'section'
    def lookups(self, request, model_admin):
        return section_choices

    def queryset(self, request, queryset):
        # If the filter is actually selected, apply it
        if self.value():
            return queryset.filter(common_profile__college__section=self.value())

class ModifiedUserAdmin(UserenaAdmin):
    """This changes the way the admin websites (both the main and deanship
ones) deal with the User model."""
    list_display = ('username', 'get_ar_full_name',
                    'get_en_full_name', 'get_college', 'student_id',
                    'badge_number', 'email', 'mobile_number',
                    'is_active', 'is_coordinator', 'date_joined')
    change_form_template = 'loginas/change_form.html'
    list_filter = (EmployeeFilter, CoordinatorFilter, CollegeFilter,
                   SectionFilter)
    actions = [make_active]
    search_fields= ('username', 'email',
                    'common_profile__en_first_name',
                    'common_profile__en_middle_name',
                    'common_profile__en_last_name',
                    'common_profile__ar_first_name',
                    'common_profile__ar_middle_name',
                    'common_profile__ar_last_name',
                    'common_profile__alternative_email',
                    'common_profile__student_id',
                    'common_profile__badge_number',
                    'common_profile__mobile_number',
                    'common_profile__en_first_name',
                    'common_profile__en_middle_name',
                    'common_profile__en_last_name',
                    'common_profile__ar_first_name',
                    'common_profile__ar_middle_name',
                    'common_profile__ar_last_name',
                    'common_profile__badge_number',
                    'common_profile__job_description')
    inlines = [CommonProfileInline,]

    def has_module_permission(self, request, obj=None):
        return media.utils.is_media_coordinator_or_deputy(request.user) or \
               clubs.utils.is_presidency_coordinator_or_deputy(request.user) or \
               request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return media.utils.is_media_coordinator_or_deputy(request.user) or \
               clubs.utils.is_presidency_coordinator_or_deputy(request.user) or \
               request.user.is_superuser

    def is_coordinator(self, obj):
        return obj.coordination.current_year().exists()
    is_coordinator.boolean = True
    is_coordinator.short_description = u"منسق؟"

    def get_en_full_name(self, obj):
        return utils.get_user_en_full_name(obj)
    get_en_full_name.short_description = u"الاسم الإنجليزي الكامل"

    def get_ar_full_name(self, obj):
        return utils.get_user_en_full_name(obj)
    get_ar_full_name.short_description = u"الاسم العربي الكامل"

    def get_college(self, obj):
        return utils.get_user_college(obj)

    def student_id(self, obj):
        try:
            return obj.common_profile.student_id
        except ObjectDoesNotExist:
            return

    def badge_number(self, obj):
        try:
            return obj.common_profile.badge_number
        except ObjectDoesNotExist:
            return

    def mobile_number(self, obj):
        try:
            return obj.common_profile.mobile_number
        except ObjectDoesNotExist:
            return

user_list_admin = UserListAdmin("User List Admin")
admin.site.unregister(User)
admin.site.register(User, ModifiedUserAdmin)
user_list_admin.register(User, ModifiedUserAdmin)
