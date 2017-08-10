# -*- coding: utf-8  -*-
from django.contrib import admin
from . import models

class TeamAdmin(admin.ModelAdmin):
    #to be continued?
    list_filter = ['year', 'city', 'gender']
    list_display = ['ar_name', 'leader', 'city']
    search_fields = ['ar_name', 'en_name', 'year', 'city']

admin.site.register(models.Team, TeamAdmin)