# -*- coding: utf-8  -*-
from django.db import models

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
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"إعلان"
        verbose_name_plural = u"الإعلانات"