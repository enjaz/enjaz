# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User

from clubs.models import College, college_choices
from core.models import StudentClubYear
from studentguide.managers import GuideQuerySet, RequestQuerySet, ReportQuerySet, FeedbackQuerySet

MAXIMUM_GUIDE_STUDENTS = 8

# Student Guide

class GuideProfile(models.Model):
    user = models.ForeignKey(User, null=True,
                             on_delete=models.SET_NULL,
                             verbose_name=u"المستخدم",
                             related_name="guide_profiles")
    assessor = models.ForeignKey(User, null=True, blank=True,
                                 related_name="studentguide_assessments",
                                 on_delete=models.SET_NULL,
                                 default=None, verbose_name=u"المُقيّم",
                                 limit_choices_to={'common_profile__is_student':
                                                   True})
    avatar = models.ImageField(u"صورة رمزية", upload_to='studentguide/avatar/')
    activities = models.TextField(u"المشاريع والنشاطات السابقة", help_text=u"ما أبرز الأنشطة والمشاريع التي سبق أن عملت عليها؟ هذا يتضمن أي أبحاث، أو أعمال كان لك دورٌ أساسيٌ فيها.")
    academic_interests = models.TextField(u"الاهتمامات الأكاديمية", help_text=u"في السياق الأكاديمي، ما الذي يستهويك؟")
    nonacademic_interests = models.TextField(u"الاهتمامات غير  الأكاديمية", help_text=u"بعيدا عن التحصيل الأكاديمي، ما الذي يشغلك؟")
    batch = models.PositiveSmallIntegerField(verbose_name=u"الدفعة")
    year = models.ForeignKey(StudentClubYear, null=True,
                             on_delete=models.SET_NULL, default=None,
                             verbose_name=u"السنة")
    tags = models.ManyToManyField('Tag', verbose_name=u"الوسوم",
                                  related_name="guide_profiles",
                                  help_text=u"يمكنك اختيار أكثر من وسم.")
    is_available = models.BooleanField(default=True,
                                       verbose_name=u"متاح؟")
    is_deleted = models.BooleanField(verbose_name=u"محذوف؟",
                                     default=False)
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True)
    objects = GuideQuerySet.as_manager()
    class Meta:
        verbose_name = u"ملف مرشد طلابي"
        verbose_name_plural = u"ملفات المرشدين الطلابيين"

    def update_availability_status(self):
        if self.guide_requests.filter(requester_status='A',
                                      guide_status='A').count() >= MAXIMUM_GUIDE_STUDENTS:
            self.is_available = False
        else:
            self.is_available = True

    def get_last_report(self):
        if self.student_guide_reports.exists():
            return self.student_guide_reports.order_by("submission_date").last()

    def __unicode__(self):
        return self.user.common_profile.get_ar_full_name()

class Request(models.Model):    
    user = models.ForeignKey(User, null=True,
                             on_delete=models.SET_NULL,
                             verbose_name=u"الطالب المستجد",
                             related_name="guide_requests")
    guide = models.ForeignKey(GuideProfile, null=True,
                                  on_delete=models.SET_NULL,
                                  verbose_name=u"المرشد الطلابي",
                                  related_name="guide_requests")
    guide_status_choices = (
        ('P', u'معلق'),
        ('A', u'مقبول'),
        ('R', u'مرفوض'),
    )
    guide_status = models.CharField(max_length=1, verbose_name=u"الحالة المرشد",
                                    default='P',
                                    choices=guide_status_choices)
    guide_status_date = models.DateTimeField(u'تاريخ حالة المرشد',
                                             null=True, blank=True,
                                             default=None)
    requester_status_choices = (
        ('A', u'معتمدة'),
        ('C', u'ملغاة'),
    )
    requester_status = models.CharField(max_length=1,
                                        verbose_name=u"الحالة مقدم الطلب",
                                        default='A',
                                        choices=requester_status_choices)
    requester_status_date = models.DateTimeField(u'تاريخ حالة مقدم الطلب',
                                                 null=True, blank=True,
                                                 default=None)
    interests = models.TextField(u"الاهتمامات", help_text=u"ما المجالات التي تريد تطوير نفسك فيها؟")
    batch = models.PositiveSmallIntegerField(verbose_name=u"الدفعة")
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True)

    objects = RequestQuerySet.as_manager()

    def get_status(self):
        if self.guide_status == 'P' and self.requester_status == 'A':
            return u"تنتظر موافقة المرشد"
        elif self.guide_status == 'P' and self.requester_status == 'C':
            return u"ألغها مقدم الطلب قبل موافقة المرشد"
        elif self.guide_status == 'A' and self.requester_status == 'A':
            return u"معتمدة"
        elif self.guide_status == 'A' and self.requester_status == 'C':
            return u"ألغها مقدم الطلب بعد موافقة المرشد"
        elif self.guide_status == 'R' and self.requester_status == 'A':
            return u"ألغها المرشد"

    def __unicode__(self):
        return self.user.common_profile.get_en_full_name()

    class Meta:
        verbose_name = u"طلب إرشاد"
        verbose_name_plural = u"طلبات الإرشاد"

class Report(models.Model):
    guide = models.ForeignKey(GuideProfile, null=True,
                                  on_delete=models.SET_NULL,
                                  verbose_name=u"المرشد الطلابي",
                                  related_name="student_guide_reports")
    session_date = models.DateField(u"تاريخ الجلسة")
    session_location = models.CharField(max_length=200,
                                        verbose_name=u"مكان الجلسة")
    session_duration = models.CharField(max_length=200,
                                        verbose_name=u"مدة الجلسة")
    means_of_communication = models.CharField(max_length=200,
                                              verbose_name=u"وسيلة التواصل المعتمدة مع الطلبة المستفيدين")
    points_discussed = models.TextField(u"المشكلات والقضايا التي نوقشت")
    plans_suggested = models.TextField(u"الخطط والحلول التي وُضعت")
    issues_faced = models.TextField(u"هل من صعوبات في عقد الجلسة؟",
                                    blank=True, default="", help_text=u"اختياري")
    other_comments = models.TextField(u"ملاحظات أخرى", blank=True, help_text=u"اختياري")
    next_session_date = models.DateField(u"تاريخ الجلسة القادمة", blank=True,
                                         null=True, help_text=u"اختياري")
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)
    was_revised = models.BooleanField(u"روجع؟", default=False)
    revision_date = models.DateTimeField(u'تاريخ المراجعة', null=True,
                                         default=None)
    is_deleted = models.BooleanField(verbose_name=u"محذوف؟",
                                     default=False)
    objects = ReportQuerySet.as_manager()
    def __unicode__(self):
        return self.guide.user.common_profile.get_ar_full_name()

class Feedback(models.Model):
    submitter = models.ForeignKey(User, null=True,
                                  on_delete=models.SET_NULL,
                                  verbose_name=u"المستخدم",
                                  related_name="arshidni_feedback")
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)
    text = models.TextField(u"ملاحظتك")
    guide = models.ForeignKey(GuideProfile, null=True,
                              on_delete=models.SET_NULL,
                              verbose_name=u"المرشد الطلابي")
    objects = FeedbackQuerySet.as_manager()
    def __unicode__(self):
        return self.submitter.common_profile.get_ar_full_name()

class Tag(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name=u"الاسم")
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)
    code_name = models.CharField(max_length=50,
                                 verbose_name=u"الاسم البرمجي",
                                 help_text=u"حروف لاتينية صغيرة وأرقام")
    image = models.FileField(upload_to='studentguide/tags/', blank=True, null=True)

    def __unicode__(self):
        return self.name
