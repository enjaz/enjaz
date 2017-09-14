# coding=utf-8
import ckeditor.fields
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import DEFINITE_PLURAL_STUDENT_GENDER_CHOICES


class AbstractRequest(models.Model):
    """
    This is a base class that includes fields common to both `ActivityRequest`
    and `ActivityCancelRequest`
    """
    submitter_team = models.ForeignKey(
        'teams.Team',
        related_name='%(class)ss',
        verbose_name=_(u"الفريق المقدّم للطلب"),
    )
    submitter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)ss',
        verbose_name=_(u"مقدّم الطلب"),
        on_delete=models.SET_NULL, null=True,
    )
    submission_datetime = models.DateTimeField(
        _(u"وقت تقديم الطلب"),
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class ActivityRequest(AbstractRequest):
    """
    A request to conduct an activity
    """
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

    category = models.ForeignKey(
        'activities.Category',
        related_name='activity_requests',
        verbose_name=_(u"التصنيف"),
        on_delete=models.SET_NULL, null=True,
        limit_choices_to={'category__isnull': True},  # If the category has sub-categories, don't show it.
    )

    # Descriptive fields  # TODO: These should be implemented using a more generic way!
    description = models.TextField(_(u"الوصف"))
    goals = models.TextField(_(u"الأهداف"))

    inside_collaborators = models.TextField(_(u"الجهات المتعاونة من داخل الجامعة"))
    outside_collaborators = models.TextField(_(u"الجهات المتعاونة من خارج الجامعة"))

    organizer_count = models.PositiveIntegerField(_(u"عدد المنظمين"))
    participant_count = models.PositiveIntegerField(_(u"عدد المشاركين"))

    # Collaboration fields
    collaborating_teams = models.ManyToManyField(
        'teams.Team',
        related_name='collaborated_activity_requests',
        verbose_name=_(u"الفرق المتعاونة"),
    )

    # Date and location fields
    start_date = models.DateField(_(u"تاريخ البداية"))
    end_date = models.DateField(_(u"تاريخ النهاية"))
    location = models.CharField(_(u"المكان"), max_length=100)

    # Targeted population fields
    # TODO: Add an option in the form to select "all" (?)
    campus = models.ManyToManyField(
        "core.Campus",
        verbose_name=_(u"المدينة الجامعية"),
    )
    specialty = models.ManyToManyField(
        "core.Specialty",
        verbose_name=_(u"التخصص"),
    )
    gender = models.CharField(
        _(u"القسم"),
        max_length=1,
        choices=DEFINITE_PLURAL_STUDENT_GENDER_CHOICES
    )

    # This is a flag to distinguish update from creation requests
    is_update_request = models.BooleanField(
        _(u"نوع الطلب"),
        choices=(
            (False, _(u"طلب إضافة")),
            (True, _(u"طلب تعديل")),
        ),
        default=False,
    )

    @property
    def is_open(self):
        return not self.reviews.exists()  # This is a temporary implementation

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u"طلب نشاط")
        verbose_name_plural = _(u"طلبات أنشطة")


class ActivityCancelRequest(AbstractRequest):
    """
    A request to cancel an approved activity
    """
    activity = models.ForeignKey(
        'activities2.Activity',
        verbose_name=_(u"النشاط"),
        related_name="requests_canceld",

    )

    class Meta:
        verbose_name = _(u"طلب إلغاء نشاط")
        verbose_name_plural = _(u"طلبات إلغاء أنشطة")


class AbstractRequestAttachment(models.Model):
    """
    This is a base class for all kinds of 'request attachments' that accompany an activity request
    """
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
    """
    An activity may contain one or more events. Each `Event` represents a single
    continuous session on particular date, with start and end times, and a specific location.
    """
    label = models.CharField(_(u"العنوان"), max_length=50)
    description = models.CharField(_(u"الوصف"), max_length=200)
    date = models.DateField(_(u"التاريخ"))
    start_time = models.TimeField(_(u"وقت البداية"))
    end_time = models.TimeField(_(u"وقت النهاية"))
    location = models.CharField(_(u"المكان"), max_length=50)

    def __unicode__(self):
        return self.label

    class Meta:
        verbose_name = _(u"طلب فعالية")
        verbose_name_plural = _(u"طلبات فعاليات")


class DepositoryItemRequest(AbstractRequestAttachment):
    """
    A request for an item that's found in the depository.
    (See `activities.DepositoryItem`)
    """
    name = models.CharField(_(u"الاسم"), max_length=100)
    quantity = models.PositiveIntegerField(_(u"الكمية"))
    unit = models.CharField(_(u"الوحدة"), max_length=20)
    category = models.CharField(_(u"التصنيف"), max_length=40)

    def __unicode__(self):
        return self.name

    # class Meta:
    #     verbose_name = _(u"")
    #     verbose_name_plural = _(u"")


class RequirementRequest(AbstractRequestAttachment):
    """
    A request for a particular requirement needed for an activity. This could be a purchase,
     an administrative action or communication, or any requirement in general.
    """
    description = models.CharField(_(u"الوصف"), max_length=50)

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = _(u"متطلّب")
        verbose_name_plural = _(u"متطلّبات")


class FileAttachment(AbstractRequestAttachment):
    description = models.CharField(
        _(u"الوصف"),
        max_length=200,
    )
    file = models.FileField(
        _(u"الملف"),
        upload_to='approvals/file_attachments/',
    )

    def __unicode__(self):
        if self.description:
            return self.description
        return self.file.name

    class Meta:
        verbose_name = _(u"ملف مرفق")
        verbose_name_plural = _(u"ملفات مرفقة")


class ActivityRequestComment(models.Model):
    """
    A comment on an activity request thread.
    """
    thread_id = models.PositiveIntegerField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='activity_request_comments',
        verbose_name=_(u"المعلّق"),
        on_delete=models.SET_NULL, null=True,
    )
    text = models.TextField(_(u"النص"))
    submission_datetime = models.DateTimeField(
        _(u"التاريخ و الوقت"),
        auto_now_add=True
    )

    def __unicode__(self):
        return self.text[:50]  # the first 50 characters of the text

    class Meta:
        verbose_name = _(u"تعليق")
        verbose_name_plural = _(u"تعليقات")


class ActivityRequestReview(models.Model):
    """
    In order for an `ActivityRequest` to be approved, it has to be reviewed and approved
    by each team in the workflow to which the team requesting the activity refers.
    """
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
    submitter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='activity_request_reviews',
        verbose_name=_(u"المراجِع"),
        on_delete=models.SET_NULL, null=True,
    )
    submitter_team = models.ForeignKey(
        'teams.Team',
        related_name='activity_request_reviews',
        verbose_name=_(u"الفريق المراجِع"),
        on_delete=models.SET_NULL, null=True,
    )
    submission_datetime = models.DateTimeField(
        _(u"التاريخ و الوقت"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _(u"مراجَعة")
        verbose_name_plural = _(u"مراجَعات")


class RequestThread(object):
    """
    A request thread is a sequence of `ActivityRequest`'s related to the same activity.
    """
    def __init__(self, id):
        """
        A unique thread id identifies each request thread. This id is stored
        in all instances that are contained in the thread.
        """
        self.id = id
        self.requests = ActivityRequest.objects.filter(thread_id=id)
        self.comments = ActivityRequestComment.objects.filter(thread_id=id)
        self.reviews = ActivityRequestReview.objects.filter(request__in=self.requests)

    @property
    def items(self):
        import itertools
        return sorted(
            itertools.chain(self.requests, self.comments, self.reviews),
            key=lambda item: item.submission_datetime,
        )

    @property
    def name(self):
        return self.requests.first().name  # performance? (esp. in long lists)

    @property
    def is_active(self):
        return any([request.is_open for request in self.requests])

    @property
    def date_opened(self):
        return self.requests.first().submission_datetime

    @property
    def last_updated(self):
        return self.items[-1].submission_datetime

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
        Return a list of `RequestThread`s based on the passed lookups (currently only `id` and `is_active` supported)
        """
        filtered = cls._get_all_threads()

        thread_id = kwargs.get('id')
        is_active = kwargs.get('is_active')

        if thread_id:
            filtered = filter(lambda thread: thread.id == int(thread_id), filtered)

        if is_active is not None:
            filtered = filter(lambda thread: thread.is_active == is_active, filtered)

        return filtered

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
