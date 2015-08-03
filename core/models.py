# -*- coding: utf-8  -*-
from django.db import models
from django.utils import timezone

# TODO: Announcements should be moved to media
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
    # TODO: announcements should be flexible as to who can see them (eg, different announcements for different campuses)
    
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

class YearManager(models.Manager):
    def get_by_year(self, start_year, end_year):
        return self.get(start_date__year=start_year,
                        end_date__year=end_year)
    def get_current(self):
        now = timezone.now()
        return self.get(start_date__lte=now, end_date__gte=now)

class StudentClubYear(models.Model):
    submission_date = models.DateTimeField(u"تاريخ الإضافة", auto_now_add=True)
    start_date = models.DateTimeField(u"تاريخ البداية")
    end_date = models.DateTimeField(u"تاريخ النهاية")
    niqati_closure_date = models.DateTimeField(u"تاريخ إغلاق نقاطي",
                                               null=True, blank=True)
    objects = YearManager()
    def __unicode__(self):
        return "%d/%d" % (self.start_date.year, self.end_date.year)

    class Meta:
        verbose_name = u"سنة نادي"
        verbose_name_plural = u"سنوات النادي"

