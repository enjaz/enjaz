# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User

class Club(models.Model):
    name = models.CharField(max_length=200, verbose_name=u"الاسم")
    english_name = models.CharField(max_length=200, verbose_name=u"الاسم الإنجليزي")
    description = models.TextField(max_length=200, verbose_name=u"الوصف")
    email = models.EmailField(max_length=254, verbose_name=u"البريد الإلكتروني")
    parent = models.ForeignKey('self', null=True, blank=True,
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
    creation_date = models.DateTimeField('date created')
    edit_date = models.DateTimeField('date edited', auto_now=True)

    class Meta:
        permissions = (
            #("edit_club", "Can edit club details."),
        )

    def __unicode__(self):
        return self.name
