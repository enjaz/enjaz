# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from userena.models import UserenaBaseProfile


class MyProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')
    student_id = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    clubs = models.ManyToManyField('clubs.Club', null=True)
