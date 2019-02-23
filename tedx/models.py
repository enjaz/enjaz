# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

gender_choices = (
    ('F', u'أنثى'),
    ('M', u'ذكر'),
)


class Registration(models.Model):
    user = models.ForeignKey(User, null=True, blank=True,
                             related_name='tedx_registrations')
    name = models.CharField(max_length=200, verbose_name=u"اسمك",null=True, blank=True)
    gender = models.CharField(max_length=1, choices=gender_choices,
                              verbose_name=u"الجندر",null=True, blank=True)
    age = models.PositiveSmallIntegerField(verbose_name=u"عمرك",null=True, blank=True)
    mobile = models.CharField(max_length=20, verbose_name=u"رقم الجوال",null=True, blank=True)
    emial = models.EmailField(max_length=100, verbose_name=u"البريد الإلكتروني",null=True, blank=True)
    city = models.CharField(max_length=10,
                            verbose_name=u"المدينة",
                            null=True,
                            blank=True)
    fromNGH = models.BooleanField(verbose_name="هل أنت من منسوبي ومنسوبات الحرس؟",default=False)
    job_title = models.CharField(max_length=100, verbose_name=u"المسمى الوظيفي",null=True, blank=True)
    yourself = models.TextField(verbose_name=u"تحدث عن نفسك",null=True, blank=True)
    about_tedx = models.TextField(verbose_name=u"تحدث عن تدكس",null=True, blank=True)
    attend_tedx = models.BooleanField(verbose_name=u"هل سبق وحضرت تدكس؟",default=False)
    past_experience = models.TextField(verbose_name=u"تحدث عن تجربتك السابقة مع تدكس",null=True, blank=True)
    referral = models.CharField(max_length=20, verbose_name=u"كيف سمعت عن TEDxKSAUHS?",null=True, blank=True)
    expectations = models.TextField(verbose_name=u"ماذا تتوقع أن تستفيد من TEDxKSAUHS?",null=True, blank=True)
    meaning = models.TextField(verbose_name=u"ما الذي تعنيه لك عبارة لو أن؟",null=True, blank=True)
    interview = models.BooleanField(u"هل تقبل بعمل مقابلات معك قبل و بعد الحدث؟",default=False)
    take_pic = models.BooleanField(u"هل تقبل بالتصوير أثناء الحدث؟",default=False)
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
    your_interest = models.CharField(max_length=50, choices=interests_choices, verbose_name=u"اي المجالات التالية أقرب لاهتمامك؟",null=True, blank=True)
    submission = models.DateTimeField(u'تاريخ الإرسال', auto_now=True)
    modification = models.DateTimeField(u'تاريخ الإرسال', auto_now=True)
    id_code = models.CharField(max_length=30,default='')
    work_place = models.CharField(max_length=50, verbose_name=u"مكان العمل او الدراسة", null=True, blank=True)


class Game(models.Model):
    first_question = models.ForeignKey('Question', on_delete=models.CASCADE)

class Question(models.Model):
    question_text = models.TextField(default="question text", verbose_name='نص السؤال')
    title = models.CharField(default='question title', max_length=30)
    def __unicode__(self):
        return self.title

class Choice (models.Model):
    question = models.ForeignKey(Question, related_name='choices',on_delete=models.CASCADE)
    next_question = models.ForeignKey(Question, related_name="leading_choices", on_delete=models.CASCADE, null=True)
    choice_text = models.CharField(default='خيار', max_length=3159)
    title = models.CharField(default='choice title', max_length=30)
    icon = models.CharField(max_length=30, blank=True)
    flag = models.CharField(default='choice title', max_length=30, blank=True)
    def __unicode__(self):
        return self.title
