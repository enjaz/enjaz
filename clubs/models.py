# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User

section_choices = (
    ('M', u'طلاب'),
    ('F', u'طالبات'),
    ('K', u'مدينة الملك فهد'),
)
college_choices = (
    ('M', u'كلية الطب'),
    ('P', u'كلية الصيدلة'),
    ('D', u'كلية الأسنان'),
    ('B', u'كلية المهن الصحية'),
    ('A', u'كلية العلوم التطبيقية'),
)

class Club(models.Model):
    name = models.CharField(max_length=200, verbose_name=u"الاسم")
    english_name = models.CharField(max_length=200, verbose_name=u"الاسم الإنجليزي")
    description = models.TextField(verbose_name=u"الوصف")
    email = models.EmailField(max_length=254, verbose_name=u"البريد الإلكتروني")
    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name="parenthood",
                               on_delete=models.SET_NULL,
                               default=None, verbose_name=u"النادي الأب")
    coordinator = models.ForeignKey(User, null=True,
                                    blank=True,
                                    verbose_name=u"المنسق",
                                    related_name="coordination",
                                    # To exclude AnonymousUser
                                    limit_choices_to={'pk__gt': -1})
    members = models.ManyToManyField(User, null=True,
                                     verbose_name=u"الأعضاء",
                                     blank=True,
                                     related_name="memberships")
    open_membership = models.BooleanField(default=False,
                                               verbose_name=u"اسمح بالتسجيل؟")
    creation_date = models.DateTimeField('date created',
                                         auto_now_add=True)
    edit_date = models.DateTimeField('date edited', auto_now=True)

    def __unicode__(self):
        return self.name

class MembershipApplication(models.Model):
    club = models.ForeignKey(Club, related_name='club')
    user = models.ForeignKey(User, related_name='user')
    note = models.TextField(verbose_name=u"لماذا تريد الانضمام؟")
    submission_date = models.DateTimeField('date submitted',
                                           auto_now_add=True)

    class Meta:
        permissions = (
            ("view_application", "Can view all available applications."),
        )

    def __unicode__(self):
        return self.user

class Batch(models.Model):
    college = models.ForeignKey('College')
    batch_number = models.PositiveSmallIntegerField(verbose_name=u"رقم الدفعة")
    def __unicode__(self):
        return u"%s - الدفعة %d - %s" % (self.college.get_college_name_display(), self.batch_number, self.college.get_section_display())

class College(models.Model):
    section = models.CharField(max_length=1, choices=section_choices)
    college_name = models.CharField(max_length=1, choices=college_choices)

    def __unicode__(self):
        return u"%s (%s)" % (self.get_college_name_display(), self.get_section_display())
