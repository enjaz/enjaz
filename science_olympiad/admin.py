from django.contrib import admin

from .models import Inventor

class InventorAdmin(admin.ModelAdmin):
    list_filter = ['inv_category', 'is_prototype']
    list_display = ['__unicode__', 'ar_name', 'en_name', 'prototype_file', 'submission_date']
    search_fields = ['ar_name', 'en_name', 'invention_name', 'inv_category', 'summary']

admin.site.register(Inventor, InventorAdmin)
