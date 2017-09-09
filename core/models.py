# -*- coding: utf-8  -*-
from collections import namedtuple

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

import accounts.utils
from core.managers import StudentClubYearManager

# I'm not sure if a `namedtuple` is the best way to do this. However, what this attempts to do is emulate the behavior
# of an enum in other languages, since Python 2.7 doesn't support these out of the box.
# (They are supported in Python 3, however.)
_GenderMapping = namedtuple('Gender', ['male', 'female'])

# What this basically does is map our gender choice constants ('M' and 'F') to 2 variables
# (`male` and `female`) grouped under a bigger `Gender` object. The aim is to conceal our constants as much as
# possible and refer to them by their names instead. So instead of directly using 'M' and 'F', just import `Gender`
# anywhere in the project and use `Gender.male` and `Gender.female`.
# (See example below with `GENERIC_GENDER_CHOICES` AND `PLURAL_STUDENT_GENDER_CHOICES`)
# This way we only need to define our constants once and just reuse them around the place.
# It's just a much cleaner approach.
Gender = _GenderMapping(male='M', female='F')

# These choices below are meant to be used all around the project.
GENERIC_GENDER_CHOICES = (
    (Gender.male, _(u"ذكر")),
    (Gender.female, _(u"أنثى")),
)

PLURAL_STUDENT_GENDER_CHOICES = (
    (Gender.male, _(u"طلاب")),
    (Gender.female, _(u"طالبات")),
)


class Campus(models.Model):
    """
    Each campus represents one city where the student club operates.
    """
    city = models.CharField(_(u"المدينة"), max_length=30)

    def __unicode__(self):
        return self.city

    class Meta:
        verbose_name = _(u"مدينة جامعية")
        verbose_name_plural = _(u"مدن جامعية")


class Specialty(models.Model):
    """
    A specialty like Medicine or Nursing.
    """
    name = models.CharField(_(u"الاسم"), max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u"تخصص")
        verbose_name_plural = _(u"تخصصات")


# May be implemented in the future
# class Level(models.Model):
#     pass


class StudentClubYear(models.Model):
    submission_date = models.DateTimeField(u"تاريخ الإضافة", auto_now_add=True)
    start_date = models.DateTimeField(u"تاريخ البداية")
    end_date = models.DateTimeField(u"تاريخ النهاية")
    riyadh_niqati_closure_date = models.DateTimeField(u"تاريخ إغلاق نقاطي في الرياض",
                                                      null=True, blank=True)
    jeddah_niqati_closure_date = models.DateTimeField(u"تاريخ إغلاق نقاطي في جدة",
                                                      null=True, blank=True)
    alahsa_niqati_closure_date = models.DateTimeField(u"تاريخ إغلاق نقاطي في الأحساء",
                                                      null=True, blank=True)
    riyadh_closing_ceremony_date = models.DateField(u"الحفل الختامي في الرياض",
                                                    null=True, blank=True)
    jeddah_closing_ceremony_date = models.DateField(u"الحفل الختامي في جدة",
                                                    null=True, blank=True)
    alahsa_closing_ceremony_date = models.DateField(u"الحفل الختامي في الأحساء",
                                                    null=True, blank=True)
    bookexchange_close_date = models.DateField(u"تاريخ إغلاق تبادل الكتب",
                                               null=True, blank=True)
    bookexchange_open_date = models.DateField(u"تاريخ فتح تبادل الكتب",
                                              null=True, blank=True)

    objects = StudentClubYearManager()

    def __unicode__(self):
        return "%d/%d" % (self.start_date.year, self.end_date.year)

    def get_closing_ceremony_date(self, user):
        city = accounts.utils.get_user_city(user)
        if city == u'الأحساء':
            return self.alahsa_closing_ceremony_date
        elif city == u'جدة':
            return self.jeddah_closing_ceremony_date
        else:
            return self.riyadh_closing_ceremony_date

    class Meta:
        verbose_name = u"سنة نادي"
        verbose_name_plural = u"سنوات النادي"


class Publication(models.Model):
    """
    A publication by the students club, to be displayed in the 'About Students Club' page.
    """
    file = models.FileField(u"الملف", upload_to="sc-publications/")
    label = models.CharField(u"العنوان", max_length=128)
    date_added = models.DateTimeField(u"تاريخ الإضافة", auto_now_add=True)

    def __unicode__(self):
        return self.label

    class Meta:
        verbose_name = u"إصدار"
        verbose_name_plural = u"الإصدارات"


class Tweet(models.Model):
    text = models.CharField(u"النص", max_length=155)
    tweet_id = models.BigIntegerField(null=True)
    media_path = models.CharField(u"مسار الصورة المرفقة",
                                  max_length=254,
                                  blank=True, default="")
    failed_trials = models.PositiveSmallIntegerField(u"عدد المحاولات الفاشلة",
                                                     default=0)
    user = models.ForeignKey(User, null=True,
                             on_delete=models.SET_NULL)
    access = models.ForeignKey("TwitterAccess", null=True,
                               on_delete=models.SET_NULL)
    was_sent = models.BooleanField(u"أرسلت؟", default=False)
    modification_date = models.DateTimeField(u"تاريخ التعديل",
                                             auto_now=True)
    submission_date = models.DateTimeField(u"تاريخ الإضافة",
                                           auto_now_add=True)

    def __unicode__(self):
        return self.text


class TwitterAccess(models.Model):
    access_token = models.CharField(max_length=200)
    access_token_secret = models.CharField(max_length=200)
    code_name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.code_name
