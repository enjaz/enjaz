# coding=utf-8
import ckeditor.fields
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractRequest(models.Model):
    submission_datetime = models.DateTimeField(
        _(u"وقت تقديم الطلب"),
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class ActivityRequest(AbstractRequest):
    # When the activity creation request is first created, this field should initially be blank. Once
    # the request is approved, an `Activity` object is created and linked to the request via this
    # field. For activity update requests, it should be set to the activity that is going to be
    # updated.
    activity = models.ForeignKey(
        'activities2.Activity',
        verbose_name=_(u"النشاط"),
        null=True, blank=True,
        related_name="requests_created",

    )

    name = models.CharField(_(u"العنوان"), max_length=200)

    # This is a flag to distinguish update from creation requests
    is_update_request = models.BooleanField(
        _(u"نوع الطلب"),
        choices=(
            (False, _(u"طلب إضافة")),
            (True, _(u"طلب تعديل")),
        ),
        default=False,
    )

    class Meta:
        verbose_name = _(u"طلب نشاط")
        verbose_name_plural = _(u"طلبات أنشطة")


class ActivityCancelRequest(AbstractRequest):
    activity = models.ForeignKey(
        'activities2.Activity',
        verbose_name=_(u"النشاط"),
        related_name="requests_canceld",

    )

    class Meta:
        verbose_name = _(u"طلب إلغاء نشاط")
        verbose_name_plural = _(u"طلبات إلغاء أنشطة")


class AbstractRequestAttachment(models.Model):
    activity_request = models.ForeignKey(
        'approvals.ActivityRequest',
        verbose_name=_(u"طلب النشاط"),
        related_name='%(class)ss'
    )

    class Meta:
        abstract = True


class DescriptionField(AbstractRequestAttachment):
    label = models.CharField(_(u"الوصف"), max_length=50)
    value = models.CharField(_(u"القيمة"), max_length=200)

    class Meta:
        verbose_name = _(u"حقل وصفي")
        verbose_name_plural = _(u"حقول وصفية")


class EventRequest(AbstractRequestAttachment):
    label = models.CharField(_(u"العنوان"), max_length=50)
    description = models.CharField(_(u"الوصف"), max_length=200)
    date = models.DateField(_(u"التاريخ"))
    start_time = models.TimeField(_(u"وقت البداية"))
    end_time = models.TimeField(_(u"وقت النهاية"))
    location = models.CharField(_(u"المكان"), max_length=50)

    class Meta:
        verbose_name = _(u"طلب فعالية")
        verbose_name_plural = _(u"طلبات فعاليات")

class ActivityRequsetResponse(AbstractRequestAttachment):
    request = models.ForeignKey(ActivityRequest)
    is_approved = models.BooleanField()



class RequestThread(object):
    pass
