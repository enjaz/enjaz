# -*- coding: utf-8  -*-
from django.contrib import admin
from core.models import Publication, StudentClubYear, Tweet, TwitterAccess, Campus, Specialty

# Used in bulb/admin.py and events/admin.py
class ModelAdminReadOnly:
    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]

# Used in bulb/admin.py and events/admin.py
class ModelAdminReadOnly:
    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]


class PublicationAdmin(admin.ModelAdmin):
    readonly_fields = ('date_added', )
    list_display = ('label', 'file', 'date_added')
    
admin.site.register(Campus)
admin.site.register(Specialty)
admin.site.register(StudentClubYear)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Tweet)
admin.site.register(TwitterAccess)
