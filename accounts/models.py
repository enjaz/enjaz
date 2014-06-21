# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from userena.models import UserenaBaseProfile
from clubs.models import College

class MyProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='enjaz_profile')
    ar_first_name = models.CharField(max_length=30)
    ar_middle_name = models.CharField(max_length=30)
    ar_last_name = models.CharField(max_length=30)
    en_first_name = models.CharField(max_length=30)
    en_middle_name = models.CharField(max_length=30)
    en_last_name = models.CharField(max_length=30)
    college = models.ForeignKey(College, null=True,
                                on_delete=models.SET_NULL,)
    badge_number = models.IntegerField(null=True)
    student_id = models.IntegerField(null=True, blank=True)
    mobile_number = models.CharField(max_length=20)
