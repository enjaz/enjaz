# -*- coding: utf-8  -*-
from django.contrib import admin
from core.models import Announcement, Publication, StudentClubYear


class AnnouncementAdmin(admin.ModelAdmin):
    readonly_fields = ('visits', 'date_created')
    
    list_display = ('title', 'description_summary', 'url', 'visits')
    list_filter = ('type',)
    
    def description_summary(self, obj):
        if len(obj.description) <= 60:
            return obj.description
        else:
            return obj.description[0:60] + "..."
    description_summary.short_description = u"الوصف"

class PublicationAdmin(admin.ModelAdmin):
    readonly_fields = ('date_added', )
    list_display = ('label', 'file', 'date_added')
    
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(StudentClubYear)
