# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

from core.models import StudentClubYear

role_choices = (
    ('L', 'قائد/ة'),
    ('S', 'متحدثـ/ـة'),
    ('W', 'فائز/ة'),
)

section_choices =(
    ('O', 'العروض البحثية'),
    ('P', 'الملصقات البحثية'),
)

rank_choices = (
    ('1', 'المركز الأول'),
    ('2', 'المركز الثاني'),
    ('3', 'المركز الثالث'),
)

class HPCVersion(models.Model):
    name = models.CharField(u'الاسم', max_length=200)
    version_number = models.CharField(u'رقم النسخة', max_length=100, null=True, blank=True) #مثال: النسخة الخامسة
    logo = models.FileField(u"الشعار", null=True, blank=True)
    vision = models.TextField(u'الرؤية', null=True, blank=True)
    mission = models.TextField(u'الهدف', null=True, blank=True)
    other_comment = models.TextField(u'تعليق آخر', null=True, blank=True)
    year = models.OneToOneField(StudentClubYear, verbose_name=u"السنة الدراسية")

    class Meta:
        verbose_name = u"نسخة"
        verbose_name_plural = u"نسخ المؤتمر"

    def __unicode__(self):
        return self.name

class Statistic(models.Model):
    hpc_version = models.ForeignKey(HPCVersion, verbose_name=u"النسخة")
    description = models.CharField(u'الوصف', max_length=300)
    number = models.IntegerField(u'الرقم')
    icon = models.FileField(u'الأيقونة', null=True, blank=True)

    class Meta:
        verbose_name = u"إحصائية"
        verbose_name_plural = u"إحصائيات"

    def __unicode__(self):
        return self.description

class HPCPerson(models.Model):
    user = models.OneToOneField(User, verbose_name=u"المستخدمـ/ـة", blank=True, null=True)
    name = models.CharField(u'الاسم', max_length=200)
    title = models.CharField(u'اللقب', max_length=200, blank=True, null=True)
    photo = models.FileField(u"الصورة", null=True, blank=True)
    hpc_version = models.ManyToManyField(HPCVersion, verbose_name=u'النسخة',
                                    related_name='version_personnel', blank=True)
    role = models.CharField(u'دور الفرد في المؤتمر', max_length=1, choices=role_choices)

    class Meta:
        verbose_name = u"فرد من المؤتمر"
        verbose_name_plural = u"أفراد المؤتمر "

    def __unicode__(self):
        return self.name

class Winner(HPCPerson):
    section = models.CharField(u'المسار', max_length=1, choices= section_choices)
    rank = models.CharField(u'المرتبة', max_length=1, choices= rank_choices, blank=True, null=True)

    class Meta:
        verbose_name = u"فائز"
        verbose_name_plural = u"الفائزين"

    def __unicode__(self):
        return self.name