# -*- coding: utf-8  -*-
from django.db import models

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