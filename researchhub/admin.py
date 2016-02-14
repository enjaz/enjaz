from django.contrib import admin

from researchhub.models import Project, Supervisor, SkilledStudent

class ProjectAdmin(admin.ModelAdmin):
    list_filter = ["title", "field", "submitter", "submission_date"]

admin.site.register(Project, ProjectAdmin)
admin.site.register(Supervisor)
admin.site.register(SkilledStudent)
