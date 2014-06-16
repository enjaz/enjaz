from django.contrib import admin
from activities.models import Activity, Episode

class EpisodeInline(admin.StackedInline):
    model = Episode
    extra = 0
    
class ActivityAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['name', 'description']}),
#         ('Organizers',       {'fields': ['primary_club', 'secondary_clubs', 'inside_collaborators',
#                                          'outside_collaborators']}),
#     ]    
    inlines = [EpisodeInline]
    
admin.site.register(Activity, ActivityAdmin)