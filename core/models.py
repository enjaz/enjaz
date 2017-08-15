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


class Section(models.Model):
    """
    Each campus has 2 sections, one 'male' and one 'female'.
    """
    campus = models.ForeignKey(
        'core.Campus',
        related_name='sections',
        verbose_name=_(u"المدينة الجامعية")
    )
    gender = models.CharField(
        _(u"الجنس"),
        max_length=1,
        choices=PLURAL_STUDENT_GENDER_CHOICES
    )

    def __unicode__(self):
        return u"{} - {}".format(self.campus.city, self.get_gender_display())

    class Meta:
        verbose_name = _(u"قِسم")
        verbose_name_plural = _(u"أقسام")


class College(models.Model):
    """
    `College` objects are gender-specific; so an actual college may be represented by more than 1 `College` object for
    a particular campus.
       For example, the College of Medicine in Riyadh is represented by 2 `College` objects: (1) College of
       Medicine (Male), and (2) College of Medicine (Female).
    """
    campus = models.ForeignKey(
        'core.Campus',
        related_name='colleges',
        verbose_name=_(u"المدينة الجامعية")
    )
    section = models.ForeignKey(
        'core.Section',
        related_name='colleges',
        verbose_name=_(u"القِسم")
    )
    name = models.CharField(_(u"الاسم"), max_length=50)

    # We're going to be gradually moving data from the old `clubs.College` model to here. This field is
    # for maintaining a link between the old and new data. It's a temporary measure.
    old_college_object = models.OneToOneField(
        'clubs.College',
        related_name='new_college_object',
    )

    def __unicode__(self):
        return u"{} ({} - {})".format(self.name, self.campus.city, self.section.get_gender_display())

    class Meta:
        verbose_name = _(u"كلية")
        verbose_name_plural = _(u"كليات")


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


class Announcement(models.Model):
    """
    An announcement.
    """
    TYPE_CHOICES = (
        ('R', u'إعلان بحث'),
        ('E', u'إعلان جهة خارجية'),
        ('M', u'إعلان برنامج عام لنادي الطلاب'),
    )
    type = models.CharField(max_length=1,
                            choices=TYPE_CHOICES,
                            verbose_name=u"النوع")
    title = models.CharField(max_length=128,
                             verbose_name=u"العنوان")
    description = models.TextField(verbose_name=u"الوصف")
    image = models.ImageField(upload_to='announcement_images', blank=True, null=True)
    url = models.URLField(verbose_name=u"الرابط")
    visits = models.PositiveIntegerField(default=0,
                                         verbose_name=u"عدد الزيارات")
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name=u"تاريخ الإنشاء")

    # Note: announcements should be flexible as to who can see them (eg, different announcements for different campuses)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"إعلان"
        verbose_name_plural = u"الإعلانات"


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
