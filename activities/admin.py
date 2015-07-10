# -*- coding: utf-8  -*-
import datetime

from django.contrib import admin
from activities.models import Activity, Episode, Category, Evaluation, Review
from clubs.models import section_choices
from clubs.utils import get_presidency, get_deanship
from core.models import StudentClubYear

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 0

class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0

class YearFilter(admin.SimpleListFilter):
    title = u"السنة"
    parameter_name = 'year'
    def lookups(self, request, model_admin):
        years = StudentClubYear.objects.all()
        year_lookups = [(year.start_date.year, unicode(year))
                        for year in years]
        return year_lookups

    def queryset(self, request, queryset):
        if self.value():
            start_year = int(self.value())
            end_year = start_year + 1
            chosen_year = StudentClubYear.objects.get_by_year(start_year, end_year)
            return queryset.filter(primary_club__year=chosen_year)

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
            ('a', u'مقبول'),
            ('r', u'مرفوض'),
            ('p', u'معلق'),
            )

    def queryset(self, request, queryset):
        if self.value() == 'a':
            return queryset.filter(is_approved=True)
        elif self.value() == 'r':
            return queryset.filter(is_approved=False)
        elif self.value() == 'p':
            return queryset.filter(is_approved=None)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_club', 'category',
                    'submission_date', 'is_approved',
                    'get_approval_status_message', 'get_relevance_score_average',
                    'get_quality_score_average', 'get_evaluation_count')
    list_filter = [CategoryFilter, SubmissionFilter, StatusFilter, YearFilter]
    readonly_fields = ('get_relevance_score_average', 'get_quality_score_average', )
    inlines = [EpisodeInline, ReviewInline]

class EvaluationAdmin(admin.ModelAdmin):
    readonly_fields = ('relevance', 'quality')
    list_display = ('episode', 'evaluator', 'relevance', 'quality')

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Category)
admin.site.register(Evaluation, EvaluationAdmin)
