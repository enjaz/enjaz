# -*- coding: utf-8  -*-
from django import forms
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import authenticate
from django.utils.html import format_html
from certificates import forms, models, utils
from core.utils import BASIC_SEARCH_FIELDS


class CertificateListAuthenticationForm(AdminAuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active and \
           not utils.can_access_certificate_admin(user):
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
                )

class CertificateListAdmin(admin.sites.AdminSite):
    login_form = CertificateListAuthenticationForm

    def has_permission(self, request):
        return utils.can_access_certificate_admin(request.user)

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
    form = forms.CertificateForm
    list_display = ['__unicode__', 'verification_code', 'get_link']
    readonly_fields = ['object_id', 'content_type', 'image',
                       'verification_code']
    search_fields = BASIC_SEARCH_FIELDS + ['verification_code', 'texts__text']
    list_filter = ['sessions__event', 'sessions']
    actions = [regenerate_certificate]
    inlines = [CertificateTextInline]

    def has_module_permission(self, request, obj=None):
        return utils.can_access_certificate_admin(request.user)

    def has_change_permission(self, request, obj=None):
        return utils.can_access_certificate_admin(request.user)

    def get_link(self, obj):
        if obj.image:
            return format_html(u"<a href='{}'>الشهادة</span>", obj.image.url)
    get_link.short_description = "رابط الشهادة"

    def save_formset(self, request, form, formset, change):
        certificate = formset.instance
        if not change:
            if certificate.certificate_template:
                targetted_count = certificate.certificate_template.text_positions.count()
                instances = formset.save()
                current_count = len(instances)
                remaining_count = targetted_count - current_count
                if remaining_count > 0:
                    for i in range(remaining_count):
                        models.CertificateText.objects.create(certificate=certificate,
                                                              text="")
        else:
            super(CertificateAdmin, self).save_formset(request, form, formset, change)

        if certificate.certificate_template:
            certificate.regenerate_certificate()

certificate_admin = CertificateListAdmin("Certificate Admin")

admin.site.register(models.Certificate, CertificateAdmin)
certificate_admin.register(models.Certificate, CertificateAdmin)
admin.site.register(models.CertificateRequest)
admin.site.register(models.CertificateTemplate, TemplateAdmin)
