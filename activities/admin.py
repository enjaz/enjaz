# -*- coding: utf-8  -*-
import datetime

from django.contrib import admin
from activities.models import Activity, Episode, Category, Evaluation, Review
from clubs.models import section_choices
from clubs.utils import get_presidency, get_deanship


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 0

class ReviewInline(admin.StackedInline):
    model = Review
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
                return queryset.exclude(review__reviewer_club=get_presidency())
            elif self.value() == 'p':
                presidency_reviewed = queryset.filter(review__reviewer_club=get_presidency())
                deanship_unreviewed = presidency_reviewed.exclude(review__reviewer_club=get_deanship())
                return deanship_unreviewed
            elif self.value() == 'd':
                return queryset.filter(review__reviewer_club=get_deanship())

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_club', 'category',
                    'submission_date', 'is_approved_by_presidency',
                    'is_approved_by_deanship', 'get_relevance_score_average',
                    'get_quality_score_average', 'get_evaluation_count')
    list_filter = [CategoryFilter, SubmissionFilter, StatusFilter]
    readonly_fields = ('get_relevance_score_average', 'get_quality_score_average', )
    inlines = [EpisodeInline, ReviewInline]

class EvaluationAdmin(admin.ModelAdmin):
    readonly_fields = ('relevance', 'quality')
    list_display = ('episode', 'evaluator', 'relevance', 'quality')

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Category)
admin.site.register(Evaluation, EvaluationAdmin)
