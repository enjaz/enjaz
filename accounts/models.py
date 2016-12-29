# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from userena.models import UserenaBaseProfile
from clubs.models import College, city_choices, general_gender_choices

profile_type_choices = (
    ('S', u'طالبـ/ـة'),
    ('E', u'موظفـ/ـة'),
    ('N', u'خارج الجامعة'),
)


def get_gender(user):
    return 'F' # PLACEHOLDER


class CommonProfile(models.Model):
    """This model combine both: profiles for students and non-students.
       This will make our lives much easier!"""
    user = models.OneToOneField(User,
                             unique=True,
                             verbose_name=_('user'),
                             related_name='common_profile')
    is_student = models.BooleanField(default=True,
                                     verbose_name=u"طالب؟")
    profile_type =  models.CharField(max_length=1, choices=profile_type_choices,
                            verbose_name=u"نوع المستخدمـ/ـة", default="S" )
    ar_first_name = models.CharField(max_length=30,
                                     verbose_name=u'الاسم الأول')
    ar_middle_name = models.CharField(max_length=30,
                                      verbose_name=u'الاسم الأوسط')
    ar_last_name = models.CharField(max_length=30,
                                    verbose_name=u'الاسم الأخير')
    en_first_name = models.CharField(max_length=30,
                                     verbose_name=u'الاسم الأول')
    en_middle_name = models.CharField(max_length=30,
                                      verbose_name=u'الاسم الأوسط')
    en_last_name = models.CharField(max_length=30,
                                    verbose_name=u'الاسم الأخير')
    alternative_email = models.EmailField(u"البريد الإلكتروني  الشخصي البديل",
                                          blank=True)
    badge_number = models.IntegerField(null=True,
                                       verbose_name=u'رقم البطاقة الجامعية')
    mobile_number = models.CharField(max_length=20,
                                     verbose_name=u'رقم الجوال')
    city = models.CharField(max_length=20,
                            verbose_name=u"المدينة", default=u"الرياض")
    gender = models.CharField(max_length=1, choices=general_gender_choices,
                              verbose_name=u"الجندر", default="")

    canceled_twitter_connection = models.BooleanField(default=False,
                                                      verbose_name=u"ألغى طلب الربط بتويتر؟")
    # Fields specific for students
    student_id = models.IntegerField(null=True, blank=True,
                                     verbose_name=u'الرقم الجامعي')
    college = models.ForeignKey(College, null=True,
                                blank=True,
                                on_delete=models.SET_NULL,
                                verbose_name=u'الكلية')
    # Fields specific for non-students.
    job_description = models.TextField(u"المسمى الوظيفي", blank=True)
    modification_date = models.DateTimeField(auto_now=True, null=True)

    # Fields specific for non-users.
    affiliation = models.CharField(max_length=30, default="",
                                   verbose_name=u'جهة الدراسة / العمل')

    def get_ar_full_name(self):
        ar_fullname = None
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
        en_fullname = None
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


class EnjazProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                             unique=True,
                             verbose_name=_('user'),
                             related_name='enjaz_profile')
