# coding=utf-8
import ckeditor.fields
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ActivityRequest(models.Model):
    name = models.CharField(_(u"اسم النشاط"), max_length=200)
    description = ckeditor.fields.RichTextField(_(u"وصف النشاط"))

    is_update_request = models.BooleanField(default=False)  # Flag to distinguish update from creation requests

    class Meta:
        verbose_name = _(u"طلب نشاط")
        verbose_name_plural = _(u"طلبات أنشطة")


class AbstractSubRequest(models.Model):
    parent_request = models.ForeignKey(ActivityRequest, related_name='%(class)ss')

    class Meta:
        abstract = True


class EventSubRequest(AbstractSubRequest):
    label = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=50)

    class Meta:
        verbose_name = _(u"طلب فعالية")
        verbose_name_plural = _(u"طلبات فعاليات")


class ActivityCancelRequest(models.Model):
    pass


class RequestThread(object):
    pass
