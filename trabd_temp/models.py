# -*- coding: utf-8  -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Max
from django.utils import timezone


# Create your models here.
city_choices = (
    ('', 'عامة'),
    ('R', 'الرياض'),
    ('J', 'جدة'),
    ('A', 'الأحساء'),
    )


class Nomination(models.Model):
    plan = models.FileField("الخطة")
    cv = models.FileField("السيرة الذاتية")
    certificates = models.FileField(null=True, verbose_name="الشهادات والمساهمات")
    gpa = models.FloatField("المعدل الجامعي", null=True)
    user = models.ForeignKey(User, verbose_name="المرشَّح")
    position = models.TextField(verbose_name="المنصب")
    city = models.CharField("المدينة", max_length=1, blank=True,
                            default="", choices=city_choices)
    is_rejected = models.BooleanField(default=False)
    submission_date = models.DateTimeField("تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField("تاريخ التعديل", auto_now=True, null=True)

    class Meta:
        verbose_name = 'المرشحـ/ـة'
        verbose_name_plural = 'المرشحون/المرشّحات'

    def __unicode__(self):
        try:
            name = self.user.common_profile.get_ar_full_name()
        except ObjectDoesNotExist:
            # If no profile
            name = self.user.username
        return "nomination of %s for %s" % (name, self.position)