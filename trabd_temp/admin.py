# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import admin
from . import forms, models

# Register your models here.

def make_rejected(ModelAdmin, request, queryset):
    queryset.update(is_rejected=True)
make_rejected.short_description = "رفض المرشحـ/ين المختار/ين"


class NominationAdmin(admin.ModelAdmin):
    list_filter = ['is_rejected',]
    list_display = ['__unicode__', 'cv', 'plan', 'certificates', 'gpa','is_rejected', 'position']
    search_fields = ['position']

    actions = [make_rejected,]

admin.site.register(models.Nomination, NominationAdmin)
