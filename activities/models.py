# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User

from clubs.models import College

class Activity(models.Model):
    # For now, we will follow the current practice: only one club will
    # be considered the primary orginzier.  Others will be cosidered
    # secondary.
    #clubs = models.ManyToManyField('clubs.Club',
    #                               verbose_name=u"النوادي")
    primary_club = models.ForeignKey('clubs.Club', null=True,
                                     on_delete=models.SET_NULL,
                                     related_name='primary_activity',
                                     verbose_name=u"النادي المنظم")
    secondary_clubs = models.ManyToManyField('clubs.Club', blank=True,
                                            null=True,
                                            related_name="secondary_activity",
                                            verbose_name=u"الأندية المتعاونة")
    name = models.CharField(max_length=200, verbose_name=u"اسم النشاط")
    description = models.TextField(verbose_name=u"وصف النشاط")
    requirements = models.TextField(blank=True,
                                    verbose_name=u"متطلبات النشاط")
    submitter = models.ForeignKey(User, null=True,
                                  on_delete=models.SET_NULL)
    submission_date = models.DateTimeField('date submitted',
                                           auto_now_add=True)
    location = models.CharField(max_length=200,
                                verbose_name=u"المكان", blank=True)
    date = models.DateField(u'التاريخ', null=True, blank=True)
    time = models.CharField(max_length=200, verbose_name=u'الوقت',
                            blank=True)
    custom_datetime = models.TextField(verbose_name=u"تاريخ ووقت مخصّص",
                                   blank=True, help_text=u"إذا كان النشاط الذي تنوي تنظيمه دوريا أو ممتدا لفصل كامل فعبء هذه الخانة.")
    edit_date = models.DateTimeField('date edited', auto_now=True)
    is_editable = models.BooleanField(default=True)
    collect_participants = models.BooleanField(default=False,
                                               verbose_name=u"اسمح بالتسجيل؟")
    participant_colleges = models.ManyToManyField(College,
                                                  verbose_name=u"الكليات المستهدفة",
                                                  null=True, blank=True)
    inside_collaborators = models.TextField(blank=True,
                                            verbose_name=u"المتعاونون من داخل الجامعة")
    outside_collaborators = models.TextField(blank=True,
                                             verbose_name=u"المتعاونون من خارج الجامعة")
    participants = models.IntegerField(verbose_name=u"عدد المشاركين",
                                       help_text=u"العدد المتوقع للمستفيدين من النشاط")
    organizers = models.IntegerField(verbose_name=u"عدد المنظمين",
                                       help_text=u"عدد الطلاب الذين سينظمون النشاط")

    class Meta:
        permissions = (
            ("view_activity", "Can view all available activities."),
            ("directly_add_activity", "Can add activities directly, without approval."),
        )


    def __unicode__(self):
        return self.name

class Review(models.Model):
    activity = models.ForeignKey(Activity, verbose_name=u" النشاط")
    reviewer = models.ForeignKey(User, null=True,
                                 on_delete=models.SET_NULL)
    review_date = models.DateTimeField(u'تاريخ المراجعة', auto_now_add=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True)
    clubs_notes = models.TextField(blank=True,
                                   verbose_name=u"ملاحظات على الأندية")
    name_notes = models.TextField(blank=True,
                                  verbose_name=u"ملاحظات على الاسم")
    datetime_notes = models.TextField(blank=True,
                                  verbose_name=u"ملاحظات على التاريخ والوقت")
    description_notes = models.TextField(blank=True,
                                        verbose_name=u"ملاحظات على الوصف")
    requirement_notes = models.TextField(blank=True,
                                        verbose_name=u"ملاحظات على المتطلبات")
    inside_notes = models.TextField(blank=True,
                                            verbose_name=u"ملاحظات المتعاونون من داخل الجامعة")
    outside_notes = models.TextField(blank=True,
                                             verbose_name=u"ملاحظات المتعاونون من خارج الجامعة")
    participants_notes = models.TextField(blank=True,
                                            verbose_name=u"ملاحظات على عدد المشاركين")
    organizers_notes = models.TextField(blank=True,
                                        verbose_name=u"ملاحظات على عدد المنظمين")
    review_type_choices = (
        ('P', u"رئاسة نادي الطلاب"),
        ('D', u"عمادة شؤون الطلاب"),
        )
    review_type = models.CharField(max_length=1,
                                   choices=review_type_choices,
                                   verbose_name=u"نوع المراجعة")
    approval_choices = (
        (None, u"أبقِ معلقًا"),
        (True, u"اقبل"),
        (False, u"ارفض"),
        )
    is_approved = models.NullBooleanField(choices=approval_choices,
                                          verbose_name=u"الحالة")

    class Meta:
        permissions = (
            ("view_review", "Can view all available reviews."),
            ("add_deanship_review", "Can add a review in the name of the deanship."),
            ("add_presidency_review", "Can add a review in the name of the presidency."),
            ("view_deanship_review", "Can view a review in the name of the deanship."),
            ("view_presidency_review", "Can view a review in the name of the presidency."),
        )

    def __unicode__(self):
        return str(self.id)


class Participation(models.Model):
    activity = models.ForeignKey(Activity, verbose_name=u"النشاط")
    user = models.ForeignKey(User, null=True,
                             on_delete=models.SET_NULL)
    submission_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ("view_participation", "Can view all available participations."),
        )
