from django.contrib import admin
from certificates import models

class TextPositionInline(admin.TabularInline):
    model = models.TextPosition

class TemplateAdmin(admin.ModelAdmin):
    inlines = [TextPositionInline]

admin.site.register(models.Certificate)
admin.site.register(models.CertificateRequest)
admin.site.register(models.CertificateTemplate, TemplateAdmin)
