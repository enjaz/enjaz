# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User
from core.models import StudentClubYear
from clubs.models import city_choices, gender_choices, Club, College

CATEGORY_CHOICES = (
    ('CC', 'نادي كلية'),
    ('SC', 'نادي متخصص'),
    ('I', 'مبادرة'),
    ('P', 'برنامج عام'),
    ('CD', 'عمادة كلية'),
    ('SA', 'عمادة شؤون الطلاب'),
    ('P', 'رئاسة نادي الطلاب')
    )

class Team(models.Model):
    ar_name = models.CharField(max_length=200, verbose_name=u"الاسم")
    en_name = models.CharField(max_length=200, verbose_name=u"الاسم الإنجليزي")
    code_name = models.CharField(max_length=200, verbose_name=u"الاسم البرمجي")
    email = models.EmailField(max_length=254, verbose_name=u"البريد الإلكتروني")
    year = models.ForeignKey(StudentClubYear, null=True, blank=True,
                             on_delete=models.SET_NULL, default=None,
                             verbose_name=u"السنة",
                             related_name='teams_of_year')#TODO: find better name =P
    city = models.CharField(max_length=20, choices=city_choices, verbose_name=u"المدينة")
    gender = models.CharField(max_length=1, choices=gender_choices,
                              verbose_name=u"الجنس", blank=True,
                              default="")
    leader = models.ForeignKey(User, null=True,
                                    blank=True,
                                    verbose_name=u"المنسق",
                                    related_name="teams_leader",
                                    on_delete=models.SET_NULL)
    members = models.ManyToManyField(User, verbose_name=u"الأعضاء",
                                     blank=True,
                                     related_name="teams")
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES,
                               verbose_name=u"نوع الفريق")
    is_visible= models.BooleanField(default=True, verbose_name=u"مرئي؟")
    logo = models.ImageField(upload_to='teams/logos/',
                              blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name="children",
                               on_delete=models.SET_NULL,
                               default=None, verbose_name=u"النادي الأب")
                                                           #نادي أم فريق؟
    college = models.ForeignKey(College, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 default=None,
                                 verbose_name=u"الكلية",)
    description = models.TextField(verbose_name=u"الوصف", blank=True)

    class Meta:
        verbose_name = 'الفريق'
        verbose_name_plural = 'الفِرق'