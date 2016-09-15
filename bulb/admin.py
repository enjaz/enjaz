from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ObjectDoesNotExist

from bulb.models import Category, Book, NeededBook, Request, Point, Membership, Group, Recruitment
from bulb import utils

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

class MembershipAdmin(admin.TabularInline):
    model = Membership
    extra = 0
    readonly_fields = ['get_name', ]

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
    inlines = [MembershipAdmin, ]

class RecruitmentAdmin(admin.ModelAdmin):
    list_display = ['get_full_ar_name', 'get_email',
                    'get_mobile_number', 'get_college',
                    'prefers_coordination', 'prefers_team_membership',
                    'wants_book_exchange_organization',
                    'wants_dewanya_organization', 'submission_date']

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]

    def get_full_ar_name(self, obj):
        try:
            return obj.user.common_profile.get_ar_full_name()
        except ObjectDoesNotExist:
            return obj.user.username

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"

    def get_mobile_number(self, obj):
        try:
            return obj.user.common_profile.mobile_number
        except ObjectDoesNotExist:
            return
    get_mobile_number.short_description = "Mobile number"

    def get_college(self, obj):
        try:
            return obj.user.common_profile.college.get_name_display()
        except ObjectDoesNotExist:
            return
    get_college.short_description = "College"

    def has_module_permission(self, request, obj=None):
        return utils.is_bulb_coordinator_or_deputy(request.user) or \
               utils.is_bulb_member(request.user) or \
               request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return utils.is_bulb_coordinator_or_deputy(request.user) or \
               utils.is_bulb_member(request.user) or \
               request.user.is_superuser

bulb_admin = BulbAdmin("Bulb Admin")
admin.site.register(Category)
admin.site.register(Book, BookAdmin)
admin.site.register(NeededBook, NeededBookAdmin)
admin.site.register(Request)
admin.site.register(Point)
admin.site.register(Recruitment, RecruitmentAdmin)
bulb_admin.register(Recruitment, RecruitmentAdmin)
admin.site.register(Group, GroupAdmin)
