# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from clubs.models import College
from hpc.managers import RegistrationQuerySet, SessionQuerySet

user_gender_choices = (
    ('F', u'طالبة'),
    ('M', u'طالب')
)

session_gender_choices = (
    ('', u'الجميع'),
    ('F', u'طالبات'),
    ('M', u'طلاب')
)

default_choices = [(i, i) for i in range(1, 6)]

class Abstract(models.Model):
    title = models.CharField(verbose_name="Title", max_length=255)
    authors = models.TextField(verbose_name=u"Name of authors")
    university = models.CharField(verbose_name="University", max_length=255)
    college = models.CharField(verbose_name="College", max_length=255)
    presenting_author = models.CharField(verbose_name="Presenting author", max_length=255)
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(verbose_name="Phone number", max_length=20)
    level_choices = (
        ('U', 'Undergraduate'),
        ('G', 'Graduate')
        )
    level = models.CharField(verbose_name="Level", max_length=1,
                             default='', choices=level_choices)
    presentation_preference_choices = (
        ('O', 'Oral'),
        ('P', 'Poster')
        )
    presentation_preference = models.CharField(verbose_name="Presentation preference", max_length=1, choices=presentation_preference_choices)
    attachment = models.FileField(verbose_name=u"Attach the abstract", upload_to="hpc/abstract/")
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False,
                                     verbose_name=u"محذوف؟")

    def __unicode__(self):
        return self.title

class Evaluation(models.Model):
    abstract = models.OneToOneField(Abstract)
    evaluator = models.ForeignKey(User, related_name="abstract_evaluations")
    date_submitted = models.DateTimeField(auto_now_add=True)
    clear_objectives = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Is the research Objective(s) clear?")
    informative_abstract = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Is title of the ABSTRACT informative!")
    introduction = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Does the introduction cover the topic of interest!")
    clear_method = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Is the method informative and clear!")
    good_statistics = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Are the statistical methods used well described and appropriate for the purpose of the study?")
    clear_sampling = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Is the sampling technique clear and suitable to the study?")
    clear_results = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Does the result section match the methods done? Is there a result for all methods described?")
    clear_discussion = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Is the discussion clear and answers the research question?")
    good_english = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="What is your evaluation of the English language of this paper!")
    overall_evaluation = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="What is your overall evaluation of this paper?")

    def get_total_score(self):
        total_score = sum([self.clear_objectives,
                           self.informative_abstract,
                           self.introduction, self.clear_method,
                           self.good_statistics, self.clear_sampling,
                           self.clear_results, self.clear_discussion,
                           self.good_english,
                           self.overall_evaluation])
        return total_score


class Session(models.Model):
    limit = models.PositiveSmallIntegerField(null=True, blank=True,
                                             default=None)
    name = models.CharField(max_length=255)
    time_slot = models.PositiveSmallIntegerField(null=True, blank=True,
                                                 default=None)
    vma_id = models.PositiveSmallIntegerField()
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
        return self.get_ar_full_name()

class Registration(models.Model):
    user = models.OneToOneField(User, null=True, blank=True,
                                related_name='hpc2016_registration')
    nonuser = models.OneToOneField(NonUser, null=True, blank=True,
                                    related_name='hpc2016_registration')
    sessions  = models.ManyToManyField(Session, blank=True)
    moved_sessions = models.ManyToManyField(Session, blank=True,
                                            related_name="moved_registrations")
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False,
                                     verbose_name=u"محذوف؟")
    confirmation_sent = models.BooleanField(default=False,
                                            verbose_name=u"أرسلت رسالة التأكيد؟")
    reminder_sent = models.BooleanField(default=False,
                                            verbose_name=u"أرسلت رسالة التذكير؟")
    was_moved_to_vma = models.BooleanField(default=False,
                                           verbose_name=u"نقل إلى الأكاديمية؟")

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

    def __unicode__(self):
        return self.get_ar_full_name()
