# -*- coding: utf-8  -*-
from django.contrib import admin
from certificates import models
from core.utils import BASIC_SEARCH_FIELDS

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
    search_fields = BASIC_SEARCH_FIELDS + ['verification_code']
    list_filter = ['sessions__event', 'sessions']
    actions = [regenerate_certificate]
    inlines = [CertificateTextInline]

admin.site.register(models.Certificate, CertificateAdmin)
admin.site.register(models.CertificateRequest)
admin.site.register(models.CertificateTemplate, TemplateAdmin)
