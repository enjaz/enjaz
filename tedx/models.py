# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django.db import models

gender_choices = (
    ('F', u'أنثى'),
    ('M', u'ذكر'),
)


class Registration(models.Model):
    name = models.CharField(max_length=200, verbose_name=u"اسمك")
    gender = models.CharField(max_length=1, choices=gender_choices,
                              verbose_name=u"الجندر")
    age = models.PositiveSmallIntegerField(verbose_name=u"عمرك")
    mobile = models.CharField(max_length=20, verbose_name=u"رقم الجوال")
    emial = models.EmailField(max_length=100, verbose_name=u"البريد الإلكتروني")
    city = models.CharField(max_length=10,
                            verbose_name=u"المدينة")
    fromNGH = models.BooleanField(verbose_name="هل أنت منسوبي ومنسوبات الحرس؟")
    job_title = models.CharField(max_length=100, verbose_name=u"المسمى الوظيفي")
    yourself = models.TextField(verbose_name=u"تحدث عن نفسك")
    about_tedx = models.TextField(verbose_name=u"تحدث عن تدكس")
    attend_tedx = models.BooleanField(verbose_name=u"هل سبق وحضرت تدكس؟")
    past_experience = models.TextField(verbose_name=u"تحدث عن تجربتك السابقة مع تدكس")
    referral = models.CharField(max_length=20, verbose_name=u"كيف سمعت عن TEDxKSAUHS?")
    expectations = models.TextField(verbose_name=u"ما الذي تتوقعه من TEDxKSAUHS?")
    meaning = models.TextField(verbose_name=u"ما الذي تعنيه لك لو أن؟")
    interview = models.BooleanField(u"هل تقبل بعمل مقابلات معك قبل و بعد الحدث؟")
    take_pic = models.BooleanField(u"هل تقبل بالتصوير أثناء الحدث؟")
    interests_choices = (
        ('A', u'الفن'),
        ('E',u'التعليم'),
        ('H',u'الصحة'),
        ('T',u'التكنولوجيا'),
        ('S',u'الرياضة'),
        ('B',u'ريادة الأعمال'),
        ('V',u'التطوع'),
        ('M',u'التسويق'),
        ('L',u'الأدب'),

    )
    your_interest = models.CharField(max_length=50, choices=interests_choices, verbose_name=u"اي المجالات التالية أقرب لاهتمامك؟",)
    submission = models.DateTimeField(u'تاريخ الإرسال', auto_now=True)
    modification = models.DateTimeField(u'تاريخ الإرسال', auto_now=True)
