from django.contrib import admin

from researchhub.models import Project, Supervisor, SkilledStudent, Domain, Skill

class ProjectAdmin(admin.ModelAdmin):
    list_filter = ["title", "field", "submitter", "submission_date"]

admin.site.register(Project, ProjectAdmin)
admin.site.register(Supervisor)
admin.site.register(SkilledStudent)
admin.site.register(Domain)
admin.site.register(Skill)
