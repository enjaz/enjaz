# -*- coding: utf-8  -*-
import datetime

from django.contrib import admin
from activities.models import Activity, Episode, Category
from clubs.models import section_choices

class EpisodeInline(admin.StackedInline):
    model = Episode
    extra = 0

class CategoryFilter(admin.SimpleListFilter):
    title = u"التصنيف"
    parameter_name = 'published'
    def lookups(self, request, model_admin):
        return [(category.en_name, category.ar_name) for category in
                Category.objects.filter(category__isnull=True)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__en_name=self.value())

class SubmissionFilter(admin.SimpleListFilter):
    title = u"تاريخ الإرسال"
    parameter_name = 'submitted'
    def lookups(self, request, model_admin):
        return (
            ('d', u'خلال يوم واحد'),
            ('w', u'خلال أسبوع واحد'),
            ('m', u'خلال شهر واحد'),
            )
    def queryset(self, request, queryset):
        if self.value():
            if self.value() == 'd':
                time_ago = datetime.datetime.now() - datetime.timedelta(days=1)
            elif self.value() == 'w':
                time_ago = datetime.datetime.now() - datetime.timedelta(days=7)
            elif self.value() == 'm':
                time_ago = datetime.datetime.now() - datetime.timedelta(days=30)
            else: # Just in case
                time_ago = datetime.datetime.now()
            return queryset.filter(submission_date__gte=time_ago)

class StatusFilter(admin.SimpleListFilter):
    title = u"الحالة"
    parameter_name = 'status'
    def lookups(self, request, model_admin):
        return (
            ('w', u'تنتظر مراجعة الرئاسة'), # waiting
            ('p', u'راجعتها الرئاسة ولم تراجعها العمادة'), # presidency
            ('d', u'راجعتهاالرئاسة والعمادة'), # deanship
            )
    def queryset(self, request, queryset):
        if self.value():
            if self.value() == 'w':
                return queryset.exclude(review__review_type='P')
            elif self.value() == 'p':
                presidency_reviewed = queryset.filter(review__review_type='P')
                deanship_unreviewed = presidency_reviewed.exclude(review__review_type='D')
                return deanship_unreviewed
            elif self.value() == 'd':
                return queryset.filter(review__review_type='D')

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_club', 'category',
                    'submission_date', 'is_approved_by_presidency',
                    'is_approved_by_deanship')
    list_filter = [CategoryFilter, SubmissionFilter, StatusFilter]
    inlines = [EpisodeInline]
    
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Category)
