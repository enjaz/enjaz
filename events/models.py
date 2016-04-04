# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from clubs.models import Club
from events.managers import RegistrationQuerySet, SessionQuerySet

user_gender_choices = (
    ('F', u'طالبة'),
    ('M', u'طالب')
)

session_gender_choices = (
    ('', u'الجميع'),
    ('F', u'طالبات'),
    ('M', u'طلاب')
)

class Event(models.Model):
    name = models.CharField(max_length=255)
    is_english_name = models.BooleanField(u"هل اسم الحدث إنجليزي", default=False)
    code_name = models.CharField(max_length=50, default="",
                                 blank=True,
                                 verbose_name=u"الاسم البرمجي",
                                 help_text=u"حروف لاتينية صغيرة وأرقام")
    registration_opening_date = models.DateField(u"تاريخ فتح التسجيل", null=True, blank=True)
    registration_closing_date = models.DateField(u"تاريخ انتهاء التسجيل", null=True, blank=True)
    start_date = models.DateField(u"تاريخ البدء", null=True)
    end_date = models.DateField(u"تاريخ الانتهاء", null=True)
    url = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255,
                               blank=True,
                               default="KSAU_Events")
    is_on_telegram = models.BooleanField(default=True,
                                         verbose_name=u"متاح التسجيل في يوم الحدث؟")
    organizing_club = models.ForeignKey(Club)
    priorities = models.PositiveSmallIntegerField(default=1)

    def get_html_name(self):
        if self.is_english_name:
            return "<span class='english-field'>" + self.name + "</span>"
        else:
            return self.name

    def __unicode__(self):
        return self.name

class Session(models.Model):
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=255)
    limit = models.PositiveSmallIntegerField(null=True, blank=True,
                                             default=None)
    time_slot = models.PositiveSmallIntegerField(null=True, blank=True,
                                                 default=None)
    vma_id = models.PositiveSmallIntegerField(null=True, blank=True)
    vma_time_code = models.PositiveSmallIntegerField(null=True,
                                                     blank=True,
                                                     default=None)
    code_name = models.CharField(max_length=50, default="",
                                 blank=True,
                                 verbose_name=u"الاسم البرمجي",
                                 help_text=u"حروف لاتينية صغيرة وأرقام")
    gender = models.CharField(max_length=1, blank=True,
                              default='', choices=session_gender_choices)
    location = models.CharField(blank=True, default="",
                                max_length=200,
                                verbose_name=u"المكان")
    date = models.DateField(u"التاريخ", null=True)
    start_time = models.TimeField(u"وقت البداية", null=True, blank=True, default=None)
    end_time = models.TimeField(u"وقت النهاية", null=True, blank=True, default=None)
    date_submitted = models.DateTimeField(auto_now_add=True)
    for_onsite_registration = models.BooleanField(default=False,
                                                  verbose_name=u"متاح التسجيل في يوم الحدث؟")
    objects = SessionQuerySet.as_manager()

    def get_all_registrations(self):
        return (self.first_priory_registrations.all() | \
                self.second_priory_registrations.all()).distinct()

    def __unicode__(self):
        if self.gender:
            return u"%s (%s)" % (self.name, self.get_gender_display())
        else:
            return self.name

class NonUser(models.Model):
    ar_first_name = models.CharField(max_length=30, default="",
                                     blank=True,
                                     verbose_name=u'الاسم الأول')
    ar_middle_name = models.CharField(max_length=30, default="",
                                      blank=True,
                                      verbose_name=u'الاسم الأوسط')
    ar_last_name = models.CharField(max_length=30, default="",
                                    blank=True,
                                    verbose_name=u'الاسم الأخير')
    en_first_name = models.CharField(max_length=30,
                                     verbose_name='First name')
    en_middle_name = models.CharField(max_length=30,
                                      verbose_name='Middle name')
    en_last_name = models.CharField(max_length=30,
                                    verbose_name='Last name')
    gender = models.CharField(max_length=1, verbose_name=u'الجنس',
                              default='', choices=user_gender_choices)
    email = models.EmailField(verbose_name=u'البريد الإلكتروني')
    mobile_number = models.CharField(max_length=20,
                                     verbose_name=u'رقم الجوال')
    university = models.CharField(verbose_name=u"الجامعة", max_length=255)
    college = models.CharField(verbose_name=u"الكلية", max_length=255)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def get_ar_full_name(self):
        ar_fullname = ''
        try:
            # If the Arabic first name is missing, let's assume the
            # rest is also missing.
            if self.ar_first_name:
                ar_fullname = " ".join([self.ar_first_name,
                                     self.ar_middle_name,
                                     self.ar_last_name])
        except AttributeError: # If the user has their details missing
            pass

        return ar_fullname

    def get_en_full_name(self):
        en_fullname = ''
        try:
            # If the English first name is missing, let's assume the
            # rest is also missing.
            if self.en_first_name:
                en_fullname = " ".join([self.en_first_name,
                                     self.en_middle_name,
                                     self.en_last_name])
        except AttributeError: # If the user has their details missing
            pass

        return en_fullname

    def __unicode__(self):
        return self.get_en_full_name()

class Registration(models.Model):
    user = models.ForeignKey(User, null=True, blank=True,
                             related_name='event_registrations')
    nonuser = models.ForeignKey(NonUser, null=True, blank=True,
                                related_name='event_registrations')
    first_priority_sessions  = models.ManyToManyField(Session, blank=True,
                                                      related_name="first_priory_registrations")
    second_priority_sessions  = models.ManyToManyField(Session, blank=True,
                                                      related_name="second_priory_registrations")
    moved_sessions = models.ManyToManyField(Session, blank=True,
                                            related_name="moved_registrations")
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False,
                                     verbose_name=u"محذوف؟")
    confirmation_sent = models.BooleanField(default=False,
                                            verbose_name=u"أرسلت رسالة التأكيد؟")
    reminder_sent = models.BooleanField(default=False,
                                            verbose_name=u"أرسلت رسالة التذكير؟")
    certificate_sent = models.BooleanField(default=False,
                                            verbose_name=u"أرسلت الشهادة؟")
    objects = RegistrationQuerySet.as_manager()

    def get_university(self):
        if self.user:
            try:
                common_profile = self.user.common_profile
                return "KSAU-HS"
            except ObjectDoesNotExist:
                return None
        elif self.nonuser:
            return self.nonuser.university
    get_university.short_description = u"الجامعة"

    def get_college(self):
        if self.user:
            try:
                common_profile = self.user.common_profile
                return common_profile.college.get_name_display()
            except (ObjectDoesNotExist, AttributeError):
                return None
        elif self.nonuser:
            return self.nonuser.college
    get_college.short_description = u"الكلية"

    def get_email(self):
        try:
            if self.user:
                return self.user.email
        except ObjectDoesNotExist:
            pass
        return self.nonuser.email

    def get_phone(self):
        try:
            if self.user:
                return self.user.common_profile.mobile_number
        except ObjectDoesNotExist:
            pass
        try:
            return self.nonuser.mobile_number
        except AttributeError:
            return ''

    def get_ar_first_name(self):
        if self.user:
            try:
                return self.user.common_profile.ar_first_name
            except ObjectDoesNotExist:
                return self.user.username
        elif self.nonuser:
            return self.nonuser.ar_first_name

        
    def get_ar_full_name(self):
        if self.user:
            try:
                return self.user.common_profile.get_ar_full_name()
            except ObjectDoesNotExist:
                return self.user.username
        elif self.nonuser:
            return self.nonuser.get_ar_full_name()

    def get_en_full_name(self):
        if self.user:
            try:
                return self.user.common_profile.get_en_full_name()
            except ObjectDoesNotExist:
                return self.user.username
        elif self.nonuser:
            return self.nonuser.get_en_full_name()

    def get_gender(self):
        try:
            if self.user:
                return self.user.common_profile.college.gender
        except ObjectDoesNotExist:
            pass
        try:
            return self.nonuser.gender
        except AttributeError:
            return ''
        
    def __unicode__(self):
        return self.get_en_full_name()
