# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User

section_choices = (
    ('M', u'طلاب'),
    ('F', u'طالبات'),
    ('KM', u'طلاب مدينة الملك فهد الطبية'),
    ('KF', u'طالبات مدينة الملك فهد الطبية'),
)
college_choices = (
    ('M', u'كلية الطب'),
    ('A', u'كلية العلوم الطبية التطبيقية'),
    ('P', u'كلية الصيدلة'),
    ('D', u'كلية طب الأسنان'),
    ('B', u'كلية العلوم و المهن الصحية'),
    ('N', u'كلية التمريض'),
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
                                    on_delete=models.SET_NULL,
                                    # To exclude AnonymousUser
                                    limit_choices_to={'pk__gt': -1})
    members = models.ManyToManyField(User, null=True,
                                     verbose_name=u"الأعضاء",
                                     blank=True,
                                     related_name="memberships")
    employee = models.ForeignKey(User, null=True, blank=True,
                                 related_name="employee",
                                 on_delete=models.SET_NULL,
                                 default=None,
                                 verbose_name=u"الموظف المسؤول",
                                 limit_choices_to={'user_permissions__codename': 'deanship_employee'})
    # To make it easy to make it specific to a certain college
    # (e.g. for membership), let's add this field.  That's also one
    # way to filter sub-clubs and college clubs.
    college = models.ForeignKey('College', null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 default=None,
                                 verbose_name=u"الكلية",)
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
    note = models.TextField(verbose_name=u"لماذا تريد الانضمام؟",
           help_text=u"هل لديك مهارات مخصوصة؟ هل لديك أفكار لنشاطات؟")
    submission_date = models.DateTimeField('date submitted',
                                           auto_now_add=True)

    class Meta:
        permissions = (
            ("view_application", "Can view all available applications."),
        )

    def __unicode__(self):
        return self.user

class College(models.Model):
    section = models.CharField(max_length=2, choices=section_choices)
    college_name = models.CharField(max_length=1, choices=college_choices)

    def __unicode__(self):
        return u"%s (%s)" % (self.get_college_name_display(), self.get_section_display())
