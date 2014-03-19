# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    clubs = models.ManyToManyField('clubs.Club',
                                   verbose_name=u"النوادي")
    name = models.CharField(max_length=200, verbose_name=u"الاسم")
    description = models.TextField(verbose_name=u"الوصف")
    requirements = models.TextField(blank=True,
                                    verbose_name=u"المتطلبات")
    submitter = models.ForeignKey(User, null=True,
                                  on_delete=models.SET_NULL)
    submission_date = models.DateTimeField('date submitted')
    edit_date = models.DateTimeField('date edited', auto_now=True)
    approval_date = models.DateTimeField(null=True,
                                         verbose_name=u"تاريخ الاعتماد")
    # For is_approved, we have three chocies:
    #   None: Not reviewed yet.
    #   True: Accepted.
    #   False: Rejected.
    is_approved = models.NullBooleanField(default=None)
    is_editable = models.BooleanField(default=True)
    collect_participants = models.BooleanField(default=False,
                                               verbose_name=u"اسمح بالتسجيل؟")
    inside_collaborators = models.TextField(blank=True,
                                            verbose_name=u"المتعاونون من داخل الجامعة")
    outside_collaborators = models.TextField(blank=True,
                                             verbose_name=u"المتعاونون من خارج الجامعة")
    participants = models.IntegerField(verbose_name=u"عدد المشاركين")
    organizers = models.IntegerField(verbose_name=u"عدد المنظمين")

    class Meta:
        permissions = (
            ("view_activity", "Can view all available activities."),
            ("review_activity", "Can review all available activities."),
        )


    def __unicode__(self):
        return str(self.id)
