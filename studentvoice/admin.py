# -*- coding: utf-8  -*-
from django import forms

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission, Group
from django.core.exceptions import ObjectDoesNotExist

from studentvoice.models import Voice, Vote, Recipient, Response, View

class ResponseInline(admin.StackedInline):
    model = Response
    max_num = 1
    extra = 0

class VoiceInline(admin.StackedInline):
    model = Voice
    verbose_name = u"تعليق"
    verbose_name_plural = u"التعليقات"
    extra = 0

class ResponseFilter(admin.SimpleListFilter):
    title = u"الردود"
    parameter_name = 'responses'
    def lookups(self, request, model_admin):
        return (
            ('1', u'له رد'),
            ('0', u'ليس له رد'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(response__isnull=False)
        if self.value() == '0':
            return queryset.exclude(response__isnull=False)

class PublishedFilter(admin.SimpleListFilter):
    title = u"النشر"
    parameter_name = 'published'
    def lookups(self, request, model_admin):
        return (
            ('P', u'منشور'),
            ('U', u'لم يراجع بعد'),
            ('D', u'محذوف'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'P':
            return queryset.filter(is_published=True)
        elif self.value() == 'U':
            return queryset.filter(is_published=None)
        elif self.value() == 'D':
            return queryset.filter(is_published=False)

class RevisionFilter(admin.SimpleListFilter):
    """For those that were submitted by an anonymous user, and pending
revision."""
    title = u"التعليقات"
    parameter_name = 'comment'
    def lookups(self, request, model_admin):
        return (
            ('1', u'تعليقات'),
            ('0', u'مواضيع'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(parent__isnull=False)
        if self.value() == '0':
            return queryset.filter(parent__isnull=True)


class VoiceAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'get_full_name', 'submission_date', 'edit_date',
                    'is_published', 'is_editable', 'score',
                    'number_of_views', 'is_reported')
    list_filter = [ResponseFilter, PublishedFilter, RevisionFilter]
    inlines = [ResponseInline, VoiceInline]

    def get_title(self, obj):
        if obj.title:
            return obj.title
        else:
            greatest_parent = obj.get_greatest_parent()
            return u"تعليق على %s" % greatest_parent.title
    get_title.short_description = u"العنوان"

    def get_full_name(self, obj):
        try:
            return obj.submitter.common_profile.get_ar_full_name()
        except ObjectDoesNotExist:
            return obj.submitter.username
    get_full_name.short_description = u"المستخدم"

admin.site.register(Voice, VoiceAdmin)
admin.site.register(Recipient)
admin.site.register(Response)
admin.site.register(Vote)
admin.site.register(View)
