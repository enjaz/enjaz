# coding=utf-8
import ckeditor.fields
from django.core.exceptions import ObjectDoesNotExist
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
    # The thread id is used to group requests into "threads." (See `RequestThread` class below.)
    # The first request in a thread gets an automatically assigned id, and the same id is then applied to all
    # requests sharing that same thread.
    # def increment_thread_id():
    #     return ActivityRequest.objects.order_by('thread_id').last().thread_id + 1
    thread_id = models.PositiveIntegerField()

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


class ActivityRequestReview(models.Model):
    """
    In order for an `ActivityRequest` to be approved, it has to be reviewed and approved
    by each team in the workflow to which the team requesting the activity refers.
    """
    # reviewer_team = models.ForeignKey('teams.Team')
    request = models.ForeignKey(
        'approvals.ActivityRequest',
        related_name='reviews',
        verbose_name=_(u"طلب النشاط"),
    )
    is_approved = models.BooleanField(
        _(u"تم الاعتماد؟"),
        choices=(
            (True, _(u"نعم")),
            (False, _(u"لا")),
        )
    )
    review_datetime = models.DateTimeField(
        _(u"تاريخ و وقت المراجعة"),
        auto_now_add=True,
    )


class RequestThread(object):
    """
    A request thread is a sequence of `ActivityRequest`'s related to the same activity.
    """
    def __init__(self, id=None, activity_request=None, activity=None):
        """
        A `RequestThread` can be initiated using one of three options.
        :param id: The thread_id is used to initiate the thread.
        :param activity_request: Any activity request that's part of the thread can be used to initiate it.
        :param activity: Activities can also initiate `RequestThread`s
        """
        assert any([id, activity_request, activity]), "One of the three should be specified"
        assert len(filter(lambda param: param is None, [id, activity_request, activity])) == 2,\
            "Only 1 should be specified"

        # Lets focus now on initiating the thread by ID; we can work out the other 2 options later
        self.id = id
        self.requests = ActivityRequest.objects.filter(thread_id=id)

    @property
    def name(self):
        return self.requests.first().name

    def __repr__(self):
        return "<RequestThread: {}>".format(self.id)


class RequestThreadManager(object):
    """
    This serves as an interface through which request threads are retrieved and used anywhere in the project.
    """
    @classmethod
    def get(cls, **kwargs):
        filtered = cls.filter(**kwargs)
        if not filtered:
            raise ObjectDoesNotExist
        return next(iter(filtered))

    @classmethod
    def filter(cls, **kwargs):
        """
        Return a list of `RequestThread`s based on the passed lookups (currently only `id` is supported)
        """
        thread_id = kwargs.get('id')
        if thread_id:
            return filter(lambda thread: thread.id == int(thread_id), cls._get_all_threads())
        return cls._get_all_threads()

    @classmethod
    def all(cls):
        """
        Return all request threads in a python list
        """
        return cls._get_all_threads()

    @classmethod
    def _get_all_threads(cls):
        thread_ids = cls._get_all_thread_ids()
        return [RequestThread(id=thread_id) for thread_id in thread_ids]

    @classmethod
    def _get_all_thread_ids(cls):
        return list(set(ActivityRequest.objects.values_list('thread_id', flat=True)))

