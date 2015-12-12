from django.contrib import admin

from hpc.models import Abstract


class AbstractAdmin(admin.ModelAdmin):
    list_display = ['title', 'presenting_author', 'presentation_preference', 'date_submitted']
    list_filter = ['presentation_preference']

admin.site.register(Abstract, AbstractAdmin)
