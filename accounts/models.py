# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from userena.models import UserenaBaseProfile
from clubs.models import College

def get_gender(user):
    try:
        student_profile = user.student_profile
    except ObjectDoesNotExist:
        student_profile = None
    if student_profile:
        return student_profile.college.gender
    else:
        return 'M'


class EnjazProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                             unique=True,
                             verbose_name=_('user'),
                             related_name='enjaz_profile')

class EnjazBaseProfile(models.Model):
    ar_first_name = models.CharField(max_length=30,
                                     verbose_name=u'الاسم الأول')
    ar_middle_name = models.CharField(max_length=30, verbose_name=u'الاسم الأوسط')
    ar_last_name = models.CharField(max_length=30, verbose_name=u'الاسم الأخير')
    en_first_name = models.CharField(max_length=30, verbose_name=u'الاسم الأول')
    en_middle_name = models.CharField(max_length=30, verbose_name=u'الاسم الأوسط')
    en_last_name = models.CharField(max_length=30, verbose_name=u'الاسم الأخير')
    badge_number = models.IntegerField(null=True, verbose_name=u'رقم البطاقة')

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
            # If the Arabic first name is missing, let's assume the
            # rest is also missing.
            if self.en_first_name:
                en_fullname = " ".join([self.en_first_name,
                                     self.en_middle_name,
                                     self.en_last_name])
        except AttributeError: # If the user has their details missing
            pass

        return en_fullname

class StudentProfile(EnjazBaseProfile):
    user = models.OneToOneField(User,
                             unique=True,
                             verbose_name=_('user'),
                             related_name='student_profile')
    student_id = models.IntegerField(null=True, blank=True, verbose_name=u'الرقم الجامعي')
    mobile_number = models.CharField(max_length=20, verbose_name=u'رقم الجوال')
    college = models.ForeignKey(College, null=True,
                                on_delete=models.SET_NULL,
                                verbose_name=u'الكلية')

    class Meta:
        # For the admin interface.
        verbose_name = u"ملف طالب"
        verbose_name_plural = u"ملفات الطلاب"

class NonStudentProfile(EnjazBaseProfile):
    user = models.OneToOneField(User,
                             unique=True,
                             verbose_name=_('user'),
                             related_name='nonstudent_profile')
    mobile_number = models.CharField(max_length=20, blank=True, verbose_name=u"رقم الجوال (اختياري)")
    job_description = models.CharField(max_length=50,
                                       verbose_name=u"المسمى الوظيفي")
    class Meta:
        # For the admin interface.
        verbose_name = u"ملف مستخدم آخر"
        verbose_name_plural = u"ملفات المستخدمين الآخرين"
