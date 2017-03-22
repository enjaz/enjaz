# -*- coding: utf-8  -*-
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from django import forms


from events.models import Event, Session, Registration, NonUser, Abstract, AbstractFigure, TimeSlot, SessionRegistration, Initiative, InitiativeFigure, SessionGroup,CaseReport,Criterion,Evaluation

BASIC_SEARCH_FIELDS = ['user__username', 'user__email',
                       'user__common_profile__en_first_name',
                       'user__common_profile__en_middle_name',
                       'user__common_profile__en_last_name',
                       'user__common_profile__ar_first_name',
                       'user__common_profile__ar_middle_name',
                       'user__common_profile__ar_last_name',
                       'user__common_profile__student_id',
                       'user__common_profile__badge_number',
                       'user__common_profile__mobile_number',
                       'user__common_profile__en_first_name',
                       'user__common_profile__en_middle_name',
                       'user__common_profile__en_last_name',
                       'user__common_profile__ar_first_name',
                       'user__common_profile__ar_middle_name',
                       'user__common_profile__ar_last_name']

class AbstractFigureInline(admin.TabularInline):
    model = AbstractFigure
    extra = 0

class InitiativeFigureInline(admin.TabularInline):
    model = InitiativeFigure
    extra = 0


class RegistrationUniversityFilter(admin.SimpleListFilter):
    title = "University"
    parameter_name = 'university'
    def lookups(self, request, model_admin):
        return (
            ('ksauhs', 'KSAU-HS'),
            ('other', 'Others')
            )

    def queryset(self, request, queryset):
        if self.value() == 'ksauhs':
            return queryset.filter(user__isnull=False)
        elif self.value() == 'other':
            return queryset.filter(nonuser__isnull=False)

class EventFilter(admin.SimpleListFilter):
    title = "Event"
    parameter_name = 'event'
    def lookups(self, request, model_admin):
        return Event.objects.values_list('pk', 'name') 

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(first_priority_sessions__event__pk=self.value()).distinct()

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['pk', '__unicode__', 'get_university', 'get_college',
                    'date_submitted']
    list_filter = [RegistrationUniversityFilter, EventFilter]
    search_fields= ('user__username', 'user__email',
                    'user__common_profile__en_first_name',
                    'user__common_profile__en_middle_name',
                    'user__common_profile__en_last_name',
                    'user__common_profile__ar_first_name',
                    'user__common_profile__ar_middle_name',
                    'user__common_profile__ar_last_name',
                    'user__common_profile__student_id',
                    'user__common_profile__badge_number',
                    'user__common_profile__mobile_number',
                    'user__common_profile__en_first_name',
                    'user__common_profile__en_middle_name',
                    'user__common_profile__en_last_name',
                    'user__common_profile__ar_first_name',
                    'user__common_profile__ar_middle_name',
                    'user__common_profile__ar_last_name',
                    'nonuser__email',
                    'nonuser__mobile_number',
                    'nonuser__en_first_name',
                    'nonuser__en_middle_name',
                    'nonuser__en_last_name',
                    'nonuser__ar_first_name',
                    'nonuser__ar_middle_name',
                    'nonuser__ar_last_name')

class RegistrationInline(admin.StackedInline):
    model = Registration
    extra = 1
    max_num = 1
    fields = ['sessions']
    
class NonUserAdmin(admin.ModelAdmin):
    list_display = ['pk', '__unicode__', 'university', 'college',
                    'with_deleted_registration', 'date_submitted']
    search_fields= ('email',
                    'en_first_name',
                    'en_middle_name',
                    'en_last_name',
                    'ar_first_name',
                    'ar_middle_name',
                    'ar_last_name')

    def with_deleted_registration(self, obj):
        return obj.hpc2016_registration.is_deleted
    with_deleted_registration.boolean = True

    inlines = [RegistrationInline]

class AbstractAdmin(admin.ModelAdmin):
    search_fields = BASIC_SEARCH_FIELDS + ["title"]
    list_filter = ["event"]
    inlines = [AbstractFigureInline]
    filter_horizontal = ('evaluators',)
    introduction = forms.CharField(widget=CKEditorWidget())

class InitiativeAdmin(admin.ModelAdmin):
    inlines = [InitiativeFigureInline]

class SessionGroupAdmin(admin.ModelAdmin):
    list_filter = ['event']
    list_display = ['title', 'event']
    
admin.site.register(Event)
admin.site.register(Session)
admin.site.register(CaseReport)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(NonUser, NonUserAdmin)
admin.site.register(Abstract, AbstractAdmin)
admin.site.register(TimeSlot)
admin.site.register(SessionGroup, SessionGroupAdmin)
admin.site.register(SessionRegistration)
admin.site.register(Initiative, InitiativeAdmin)
admin.site.register(Criterion)
admin.site.register(Evaluation)



