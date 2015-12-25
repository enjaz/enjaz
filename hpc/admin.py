from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from hpc.models import Abstract, Session, Registration

class UniversityFilter(admin.SimpleListFilter):
    title = "University"
    parameter_name = 'university'
    def lookups(self, request, model_admin):
        return (
            ('ksauhs', 'KSAU-HS'),
            ('other', 'Others')
            )

    def queryset(self, request, queryset):
        if self.value() == 'ksauhs':
            return queryset.filter(university='KSAU-HS')
        elif self.value() == 'other':
            return queryset.exclude(university='KSAU-HS')

class EvaluationFilter(admin.SimpleListFilter):
    title = "Evaluation"
    parameter_name = 'evaluation'
    def lookups(self, request, model_admin):
        return (
            ('evaluated', 'Evaluated'),
            ('pending', 'Pending')
            )

    def queryset(self, request, queryset):
        if self.value() == 'evaluated':
            return queryset.filter(evaluation__isnull=False)
        elif self.value() == 'pending':
            return queryset.filter(evaluation__isnull=True)

class AbstractAdmin(admin.ModelAdmin):
    list_display = ['title', 'university', 'college',
                    'presentation_preference', 'date_submitted',
                    'was_evaluated']
    list_filter = ['presentation_preference', 'level',
                   UniversityFilter, EvaluationFilter]

    def was_evaluated(self, obj):
        try:
            evaluation = obj.evaluation
            return True
        except ObjectDoesNotExist:
            return False
    was_evaluated.boolean = True

admin.site.register(Abstract, AbstractAdmin)
admin.site.register(Session)
admin.site.register(Registration)
