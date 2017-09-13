# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from core.models import StudentClubYear
from clubs.models import city_choices, gender_choices, Club, College

CATEGORY_CHOICES = (
    ('CC', _(u'نادي كلية')),
    ('SC', _(u'نادي متخصص')),
    ('I', _(u'مبادرة')),
    ('P', _(u'برنامج عام')),
    ('CD', _(u'عمادة كلية')),
    ('SA', _(u'عمادة شؤون الطلاب')),
    ('P', _(u'رئاسة نادي الطلاب'))
    )
POSITION_CHOICES = (
    ('L', _(u'ممثلـ/ـة الفريق')),
    ('VL', _(u'نائب ممثلـ/ـة الفريق')),
    ('SR', _(u'الممثلـ/ـة الإعلاميـ/ـة للفريق')),
    ('AM', _(u'عضو/ة فعالـ/ـة')),
    ('M', _(u'عضو/ة')),
    )

class Team(models.Model):
    ar_name = models.CharField(max_length=200, verbose_name=_(u"الاسم"))
    en_name = models.CharField(max_length=200, verbose_name=_(u"الاسم الإنجليزي"))
    code_name = models.CharField(max_length=200, verbose_name=_(u"الاسم البرمجي"))
    email = models.EmailField(max_length=254, verbose_name=_(u"البريد الإلكتروني"))
    year = models.ForeignKey(StudentClubYear, null=True, blank=True,
                             on_delete=models.SET_NULL, default=None,
                             verbose_name=_(u"السنة"),
                             related_name='teams_of_year')#TODO: find better name =P
    city = models.CharField(max_length=20, choices=city_choices, verbose_name=_(u"المدينة"))
    gender = models.CharField(max_length=1, choices=gender_choices,
                              verbose_name=_(u"الجنس"), blank=True,
                              default="")
    leader = models.ForeignKey(User, null=True,
                                    blank=True,
                                    verbose_name=_(u"المنسق"),
                                    related_name="teams_leader",
                                    on_delete=models.SET_NULL)
    members = models.ManyToManyField(User, through="Membership",
                                     verbose_name=_(u"الأعضاء"),
                                     blank=True)
    is_open = models.BooleanField(default=True, verbose_name=_(u"مفتوح للتسجيل؟"))
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES,
                               verbose_name=_(u"نوع الفريق"))
    is_visible= models.BooleanField(default=True, verbose_name=_(u"مرئي؟"))
    logo = models.ImageField(upload_to='teams/logos/',
                              blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name="children",
                               on_delete=models.SET_NULL,
                               default=None, verbose_name=_(u"النادي الأب"))
                                                           #نادي أم فريق؟
    college = models.ForeignKey(College, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 default=None,
                                 verbose_name=_(u"الكلية"))
    description = models.TextField(verbose_name=_(u"الوصف"), blank=True)

    def __unicode__(self):
        return self.ar_name

    class Meta:
        verbose_name = 'الفريق'
        verbose_name_plural = 'الفِرق'

    def get_absolute_url(self):
        return "/teams/%s/" % self.code_name

class Membership(models.Model):
    member = models.ForeignKey(User, verbose_name=_(u"العضو"))
    team = models.ForeignKey(Team, verbose_name=_(u"الفريق"))
    accepted = models.BooleanField(default=False)
    registration_date = models.DateTimeField(_(u"تاريخ التسجيل"), auto_now_add=True)
    modification_date = models.DateTimeField(_(u"تاريخ التعديل"), auto_now=True, null=True)

    class Meta:
        verbose_name = 'العضوية'
        verbose_name_plural = 'العضويات'

class Position(models.Model):
    team= models.ForeignKey(Team)
    user = models.ForeignKey(User, verbose_name=_(u"المستخدم"))
    position = models.CharField(max_length=2, choices=POSITION_CHOICES, default='M', verbose_name=_(u"لمنصب"))