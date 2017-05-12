# -*- coding: utf-8  -*-
from django import forms
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import authenticate
from certificates import models
from core.utils import BASIC_SEARCH_FIELDS
import clubs.utils
import events.utils
import media.utils

def has_access(user):
    return media.utils.is_media_coordinator_or_deputy(user) or \
        clubs.utils.is_presidency_coordinator_or_deputy(user) or \
        events.utils.get_user_organizing_events(user).exists()  or \
        user.is_superuser

class CertificateListAuthenticationForm(AdminAuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active and \
           not has_access(user):
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
                )

class CertificateListAdmin(admin.sites.AdminSite):
    login_form = CertificateListAuthenticationForm

    def has_permission(self, request):
        return has_access(request.user)

class TextPositionInline(admin.TabularInline):
    model = models.TextPosition

class CertificateTextInline(admin.TabularInline):
    model = models.CertificateText
    extra = 0

class TemplateAdmin(admin.ModelAdmin):
    inlines = [TextPositionInline]

def regenerate_certificate(modeladmin, request, queryset):
    for certificate in queryset:
        certificate.regenerate_certificate()
regenerate_certificate.short_description = u"أعد توليد الشهادات المُحدّدة"

class CertificateAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'verification_code']
    search_fields = BASIC_SEARCH_FIELDS + ['verification_code', 'texts__text']
    list_filter = ['sessions__event', 'sessions']
    actions = [regenerate_certificate]
    inlines = [CertificateTextInline]

    def has_module_permission(self, request, obj=None):
        return has_access(request.user)

    def has_change_permission(self, request, obj=None):
        return has_access(request.user)

certificate_admin = CertificateListAdmin("Certificate Admin")

admin.site.register(models.Certificate, CertificateAdmin)
certificate_admin.register(models.Certificate, CertificateAdmin)
admin.site.register(models.CertificateRequest)
admin.site.register(models.CertificateTemplate, TemplateAdmin)
