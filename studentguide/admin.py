# -*- coding: utf-8  -*-
from django.contrib import admin

from studentguide.models import GuideProfile, Request, Feedback, Report, Tag

common_search_fields = ('user__username', 'user__email',
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
                        'user__common_profile__ar_last_name')


class GuideAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'batch', 'get_student_count',
                    'get_pending_request_count', 'get_was_updated',
                    'is_deleted', 'submission_date')
    search_fields = common_search_fields
    def get_student_count(self, obj):
        return obj.guide_requests.filter(guide_status='A',
                                         requester_status='A').count()
    get_student_count.short_description = u"عدد الطلاب المعتمدين"

    def get_pending_request_count(self, obj):
        return obj.guide_requests.filter(guide_status='P',
                                         requester_status='A').count()
    get_pending_request_count.short_description = u"عدد الطلبات المعلقة"

    def get_was_updated(self, obj):
        return any([obj.activities, obj.academic_interests,
                    obj.nonacademic_interests])
    get_was_updated.short_description = u"حدّث الملف؟"
    get_was_updated.boolean = True
    

class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'batch', 'guide_status', 'requester_status',
                    'submission_date')
    search_fields = common_search_fields

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'guide', 'submission_date')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('guide', 'was_revised',  'submission_date')
    
admin.site.register(GuideProfile, GuideAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Tag)
