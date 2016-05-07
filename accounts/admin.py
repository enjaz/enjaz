# -*- coding: utf-8  -*-
from django import forms

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.forms import AdminAuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from userena.admin import UserenaAdmin

from clubs.models import Club, college_choices, section_choices
from accounts.models import CommonProfile
from core.models import StudentClubYear

current_year = StudentClubYear.objects.get_current()

class DeanshipAuthenticationForm(AdminAuthenticationForm):
    """A custom authentication form used in the admin app.  Based on the
original Django code."""
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = admin.forms.ERROR_MESSAGE
        params = {'username': self.username_field.verbose_name}
        deanship_group = Group.objects.get(name='deanship')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(message, code='invalid', params=params)
            # If the user isn't a deanship employee and isn't a system
            # administrator, they must not be able to use the deanship
            # admin interface.
            elif not deanship_group in self.user_cache.groups.all() and\
                 not self.user_cache.is_superuser:
                raise forms.ValidationError(message, code='invalid', params=params)
        return self.cleaned_data

class DeanshipAdmin(AdminSite):
    """This admin website is for the Student Affairs Deanship employees
to modify user permissions (e.g. who is the coordinator of which
club)."""

    login_form = DeanshipAuthenticationForm

    def has_permission(self, request):
        return request.user.has_perm('deanship_employee')

def remove_add_code_perm(modeladmin, request, queryset):
    add_code = Permission.objects.get(codename='add_code')
    for user in queryset:
        user.user_permissions.remove(add_code)
        user.save()
remove_add_code_perm.short_description = u"امنع من تسجيل نقاط"

def remove_add_book_perm(modeladmin, request, queryset):
    add_book = Permission.objects.get(codename='add_book')
    for user in queryset:
        user.user_permissions.remove(add_book)
        user.save()
remove_add_book_perm.short_description = u"امنع من إضافة الكتب"

def remove_add_bookrequest_perm(modeladmin, request, queryset):
    add_bookrequest = Permission.objects.get(codename='add_bookrequest')
    for user in queryset:
        user.user_permissions.remove(add_bookrequest)
        user.save()
remove_add_bookrequest_perm.short_description = u"امنع من طلب استعارة الكتب"

class CommonProfileInline(admin.StackedInline):
    model = CommonProfile
    max_num = 1
    extra = 0
    
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
    actions = [remove_add_code_perm, remove_add_bookrequest_perm,
               remove_add_book_perm]
    list_display = ('username', 'full_en_name', 'full_ar_name',
                    'email', 'is_active', 'is_coordinator',
                    'date_joined')
    list_filter = (EmployeeFilter, CoordinatorFilter, CollegeFilter,
                   SectionFilter)
    search_fields= ('username', 'email',
                    'common_profile__en_first_name',
                    'common_profile__en_middle_name',
                    'common_profile__en_last_name',
                    'common_profile__ar_first_name',
                    'common_profile__ar_middle_name',
                    'common_profile__ar_last_name',
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

    def is_coordinator(self, obj):
        return obj.coordination.current_year().exists()

    is_coordinator.boolean = True
    is_coordinator.short_description = u"منسق؟"

    def full_en_name(self, obj):
        try:
            return obj.common_profile.get_en_full_name()
        except ObjectDoesNotExist:
            return

    def full_ar_name(self, obj):
        try:
            return obj.common_profile.get_ar_full_name()
        except ObjectDoesNotExist:
            return

    full_en_name.short_description = u"الاسم الإنجليزي الكامل"

deanship_admin = DeanshipAdmin("Deanship Admin")
admin.site.unregister(User)
admin.site.register(User, ModifiedUserAdmin)
deanship_admin.register(User, ModifiedUserAdmin)
