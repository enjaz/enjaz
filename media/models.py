# -*- coding: utf-8  -*-
import datetime
from django.core.exceptions import ValidationError
from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from activities.models import Activity, Episode
from media.managers import BuzzManager, PollManager, FollowUpQuerySet


# Constants for media poll types

WHAT_IF = 0
HUNDRED_SAYS = 1

POLL_TYPE_CHOICES = (
    (WHAT_IF, u"ماذا لو؟"),
    (HUNDRED_SAYS, u"المئة تقول"),
)

# iCheck-plugin colors

RED = "red"
GREEN = "green"
BLUE = "blue"
AERO = "aero"
GREY = "grey"
ORANGE = "orange"
YELLOW = "yellow"
PINK = "pink"
PURPLE = "purple"

POLL_CHOICE_COLORS = (
    (RED, u"أحمر"),
    (GREEN, u"أخضر"),
    (BLUE, u"أزرق"),
    (AERO, u"رصاصي"),
    (GREY, u"رمادي"),
    (ORANGE, u"برتقالي"),
    (YELLOW, u"أصفر"),
    (PINK, u"زهري"),
    (PURPLE, u"بنفسجي"),
)

POLL_CHOICE_MAX_LENGTH = 128


class BaseComment(models.Model):
    """
    An abstract model for comments on different models of the media center.
    """
    date = models.DateTimeField(auto_now_add=True, verbose_name=u"التاريخ")
    body = models.TextField(blank=True, verbose_name=u"النص")

    class Meta:
        abstract = True

class EmployeeReport(models.Model):
    """
    A follow-up report, submitted after REPORT_DUE_AFTER days of an activity episode.
    """
    episode = models.OneToOneField(Episode, verbose_name=u"الموعد")

    submitter = models.ForeignKey(User)
    date_submitted = models.DateTimeField(auto_now_add=True,
                                      verbose_name=u"تاريخ رفع التقرير")

    # Content
    speaker = models.TextField(verbose_name=u"أسماء المتحدثين")
    quotation = models.TextField(verbose_name=u"اقتباسات من المتحدثين")
    sponsor_speech = models.TextField(verbose_name=u"كلمة الرعاة")
    prize_winner = models.TextField(verbose_name=u"أسماء المكرمين")
    winner_college_or_club = models.TextField(verbose_name=u"الكلية أو النادي الذي يتبع له المكرم")
    booth = models.TextField(verbose_name=u"أسماء الأركان المشاركة")
    sponsor = models.TextField(verbose_name=u"أسماء الجهات الراعية أو المشاركة")

    participant_count = models.IntegerField(verbose_name=u"عدد المشاركين")
    organizer_count = models.IntegerField(verbose_name=u"عدد المنظمين")
    speaker_count = models.IntegerField(verbose_name=u"عدد المتحدثين")
    lecture_count = models.IntegerField(verbose_name=u"عدد المحاضرات")
    session_count = models.IntegerField(verbose_name=u"عدد ورش العمل")
    booth_count = models.IntegerField(verbose_name=u"عدد الأركان")
    end = models.TextField(verbose_name=u"كيف إنتهى النشاط؟")

    notes = models.TextField(verbose_name=u"ملاحظات")

class FollowUpReport(models.Model):
    """
    A follow-up report, submitted after REPORT_DUE_AFTER days of an activity episode.
    """
    episode = models.OneToOneField(Episode, verbose_name=u"الموعد")
    
    submitter = models.ForeignKey(User)
    date_submitted = models.DateTimeField(auto_now_add=True,
                                      verbose_name=u"تاريخ رفع التقرير")
    
    # Content
    description = models.TextField(verbose_name=u"الوصف",
                                   help_text=u"")
    start_date = models.DateField(verbose_name=u"تاريخ البداية")
    end_date = models.DateField(verbose_name=u"تاريخ النهاية")
    start_time = models.TimeField(verbose_name=u"وقت البداية")
    end_time = models.TimeField(verbose_name=u"وقت النهاية")
    location = models.CharField(max_length=128,
                                verbose_name=u"المكان")
    organizer_count = models.IntegerField(verbose_name=u"عدد المنظمين")
    participant_count = models.IntegerField(verbose_name=u"عدد المشاركين")

    announcement_sites = models.TextField(verbose_name=u"أماكن النشر و الإعلان")
    notes = models.TextField(verbose_name=u"ملاحظات", null=True, blank=True)
    objects = FollowUpQuerySet.as_manager()
    def __unicode__(self):
        "Return the name of the parent activity followed by the number of the episode"
        return self.episode.activity.name + " #" + str(self.episode.get_index())
    
    class Meta:
        permissions = (
            ("view_followupreport", "Can view a follow-up report."),
            ("view_all_followupreports", "Can view all available follow-up reports."),
        )
        verbose_name = u"تقرير"
        verbose_name_plural = u"التقارير"
#         app_label = u"المركز الإعلامي"


class FollowUpReportImage(models.Model):
    report = models.ForeignKey(FollowUpReport, related_name='images')
    image = models.FileField(verbose_name=u"الصورة", upload_to="media/images/")


class ReportComment(BaseComment):
    author = models.ForeignKey(User, verbose_name=u"المعلِّق")
    report = models.ForeignKey(FollowUpReport, related_name="comments")

    def __unicode__(self):
        return self.report.__unicode__() + " - comment by: " + self.author.__unicode__()


class Story(models.Model):
    """
    A media coverage of a certain episode of an activity.
    """
    episode = models.OneToOneField(Episode,
                                   verbose_name=u"الموعد")
    
    writer = models.ForeignKey(User,
                               verbose_name=u"الكاتب")
    date_submitted = models.DateTimeField(auto_now_add=True,
                                      verbose_name=u"تاريخ رفع التغطية")
    
    title = models.CharField(max_length=128,
                             verbose_name=u"العنوان")
    text = models.TextField(verbose_name=u"النص")
    
    def __unicode__(self):
        return self.episode.activity.name + ": " + self.title

    class Meta:
        permissions = (
            ("view_story", "Can view all available stories."),
            ("edit_story", "Can edit any available story."),
            ("review_story", "Can review any available story."),
            ("assign_review_story", "Can assign members to review stories.")
        )
        verbose_name = u"تغطية"
        verbose_name_plural = u"التغطيات"
#         app_label = u"المركز الإعلامي"


class Article(models.Model):
    """
    An article that's submitted for publishing.
    """
    author = models.ForeignKey(User,
                               related_name=u"authored_articles",
                               verbose_name=u"الكاتب")
    author_photo = models.ImageField(
        verbose_name=u"صورة شخصية",
        upload_to='media/author_photos/',
    )
    date_submitted = models.DateTimeField(auto_now_add=True,
                                      verbose_name=u"تاريخ الرفع")
    
    title = models.CharField(max_length=128,
                             verbose_name=u"العنوان")
    text = models.TextField(
        verbose_name=u"النص",
        null=True, blank=True,
    )
    attachment = models.FileField(
        verbose_name=u"المرفقات",
        upload_to='media/articles/',
        null=True, blank=True,
    )

    STATUS_CHOICES = (
        ('A', u'تم قبوله'),
        ('P', u'ينتظر المراجعة'),
        ('E', u'ينتظر تعديلًا'),
        ('R', u'مرفوض'),
    )
    
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES,
                              default='P',
                              verbose_name=u"الحالة")
    assignee = models.ForeignKey(User,
                                 blank=True, null=True,
                                 verbose_name=u"المكلف بالمراجعة")
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        permissions = (
                ("view_article", "Can view all available articles."),
                ("review_article", "Can review any available article."),
            )
        verbose_name = u"مقال"
        verbose_name_plural = u"المقالات"
#         app_label = u"المركز الإعلامي"


class Review(models.Model):
    """
    An abstract review model.
    """
    reviewer = models.ForeignKey(User,
                                 verbose_name=u"المُراجع")
    date_reviewed = models.DateTimeField(auto_now_add=True,
                                     verbose_name=u"تاريخ المراجعة")
    notes = models.TextField(verbose_name=u"الملاحظات")
    approve = models.BooleanField(default=False)
    
    class Meta:
        abstract = True # This means this model won't have a table in the db
                        # but other models can inherit its fields


class StoryReview(Review):
    """
    A review for a story.
    """
    story = models.OneToOneField(Story,
                                 verbose_name=u"التغطية")
    class Meta:
        verbose_name = u"مراجعة تغطية"
        verbose_name_plural = u"مراجعات التغطيات"
#         app_label = u"المركز الإعلامي"


class ArticleReview(Review):
    """
    A review for an article.
    """
    article = models.ForeignKey(Article,
                                verbose_name=u"المقال")
    class Meta:
        verbose_name = u"مراجعة مقال"
        verbose_name_plural = u"مراجعات المقالات"
#         app_label = u"المركز الإعلامي"


class Task(models.Model):
    """
    An abstract task class.
    """
    assigner = models.ForeignKey(User,
                                 verbose_name="المعيِّن")
    date_assigned = models.DateTimeField(auto_now_add=True,
                                         verbose_name="تاريخ التعيين")
    completed = models.BooleanField(default=False)
    
    class Meta:
        abstract = True


class StoryTask(Task):
    """
    A task to write a story.
    """
    episode = models.OneToOneField(Episode)
    assignee = models.ForeignKey(User,
                                 related_name="assigned_storytasks",
                                 verbose_name="المعيَّن")
    story = models.OneToOneField(Story, blank=True, null=True)
    
    def __unicode__(self):
        return self.episode.__unicode__()
    
    class Meta:
        verbose_name = u"مهمة تغطية"
        verbose_name_plural = u"مهمات التغطيات"
#         app_label = u"المركز الإعلامي"


# class ArticleTask(Task):
#     """
#     A task to review or edit a task.
#     """
#     article = models.OneToOneField(Article)
#     
#     def __unicode__(self):
#         return self.article.__unicode__()

# The following models are for creating custom tasks to be assigned to the media center
# members
# Based partially on models from django-todo app:
# Check: https://github.com/shacker/django-todo/


class CustomTask(Task):
    ## list = models.ForeignKey(List)
    # created_date = models.DateField(auto_now=True, auto_now_add=True)
    # completed = models.BooleanField()
    # created_by = models.ForeignKey(User, related_name='todo_created_by')
    # assigned_to = models.ForeignKey(User, related_name='todo_assigned_to')
    ## priority = models.PositiveIntegerField(max_length=3)
    assignee = models.ForeignKey(User,
                                 related_name="assigned_tasks",
                                 verbose_name="المعيَّن")
    title = models.CharField(max_length=140, verbose_name=u"العنوان")
    description = models.TextField(blank=True, null=True, verbose_name=u"الوصف")
    due_date = models.DateField(blank=True, null=True, verbose_name=u"التاريخ المطلوب")
    completed_date = models.DateField(blank=True, null=True, verbose_name=u"تاريخ الإنهاء")

    # Model method: Has due date for an instance of this object passed?
    def is_overdue(self):
        "Returns whether the custom task's due date has passed or not."
        if self.due_date and datetime.date.today() > self.due_date:
            return True
        else:
            return False

    def __unicode__(self):
        return self.title

    # Auto-set the custom creation / completed date
    def save(self, *args, **kwargs):
        # If custom task is being marked complete, set the completed_date
        if self.completed:
            self.completed_date = datetime.datetime.now()
        super(CustomTask, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"مهمة"
        verbose_name_plural = u"المهام"


class TaskComment(BaseComment):
    """
    Not using Django's built-in comments because we want to be able to save
    a comment and change task details at the same time. Rolling our own since it's easy.
    """
    author = models.ForeignKey(User, verbose_name=u"المعلق")
    task = models.ForeignKey(CustomTask, verbose_name=u"المهمة")

    def __unicode__(self):
        return '%s, %s - %s' % (
            self.task,
            self.author,
            self.date,
        )

    class Meta:
        verbose_name = u"تعليق على مهمة"
        verbose_name_plural = u"التعليقات على المهام"




class Poll(models.Model):
    """
    Poll class that has 2 types:
    * What-if: an open-ended question which expects comments on a hypothetical scenario.
    * Hundred-says: a vote with several choices
    """
    poll_type = models.IntegerField(choices=POLL_TYPE_CHOICES, verbose_name=u"النوع")
    title = models.CharField(max_length=128, verbose_name=u"العنوان")
    text = models.TextField(verbose_name=u"النص")
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="media/pollimages/", null=True, blank=True)
    open_date = models.DateTimeField(verbose_name=u"موعد الفتح")
    close_date = models.DateTimeField(verbose_name=u"موعد الإغلاق")
    creator = models.ForeignKey(User)

    objects = PollManager()

    def is_active(self):
        return self.open_date <= timezone.now() < self.close_date

    def is_past(self):
        return self.close_date <= timezone.now()

    def is_upcoming(self):
        return timezone.now() < self.open_date

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"تصويت"
        verbose_name_plural = u"التصويتات"


class PollChoice(models.Model):
    poll = models.ForeignKey(Poll, related_name="choices")
    value = models.CharField(verbose_name= u"النص", max_length=POLL_CHOICE_MAX_LENGTH)
    color = models.CharField(verbose_name= u"اللون", max_length=128, choices=POLL_CHOICE_COLORS,
                             default=GREEN)  # stores iCheck-plugin color values e.g. blue,
                                             # green, red, grey, aero, etc.

    def get_response_count(self):
        """
        If the poll has responses, return the number of responses that chose the current response.
        """
        response_count = self.poll.responses.count()
        if response_count > 0:
            return self.poll.responses.filter(choice=self).count()
        else:
            return 0

    def get_response_percent(self):
        """
        If the poll has responses, return the percentage of responses that chose the current response.
        """
        response_count = self.poll.responses.count()
        if response_count > 0:
            return float(self.poll.responses.filter(choice=self).count()) * 100 / response_count
        else:
            return 0.0

    def __unicode__(self):
        return self.value

    class Meta:
        verbose_name = u"خيار"
        verbose_name_plural = u"الخيارات"


class PollResponse(models.Model):
    """
    A response to a poll that has choices (Hundred-says poll)
    """
    user = models.ForeignKey(User)
    poll = models.ForeignKey(Poll, related_name="responses")
    date = models.DateTimeField(auto_now_add=True)
    choice = models.ForeignKey(PollChoice)

    def __unicode__(self):
        return self.poll.title + " - response by:  " + self.user.__unicode__()

    class Meta:
        unique_together = (('poll', 'user'), )  # No user can submit more that one response


class PollComment(BaseComment):
    """
    A comment on a poll
    """
    author = models.ForeignKey(User)
    poll = models.ForeignKey(Poll, related_name="comments")

    def __unicode__(self):
        return self.poll.title + " - comment by: " + self.author.__unicode__()

class Buzz(models.Model):
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name=u"تاريخ الإرسال")
    submitter = models.ForeignKey(User)
    body = models.TextField(blank=True, verbose_name=u"النص")
    title = models.CharField(max_length=128, verbose_name=u"العنوان")
    announcement_date = models.DateTimeField(verbose_name=u"وقت الإعلان")
    is_deleted = models.BooleanField(default=False)
    is_push = models.BooleanField(default=False, verbose_name=u"إعلان عام؟")
    colleges = models.ManyToManyField('clubs.College', verbose_name=u"الكليات المستهدفة",
                                      blank=True)
    image = models.ImageField(upload_to="media/buzzimages/", null=True, blank=True, verbose_name=u"الصورة")
    objects = BuzzManager()

    def is_published(self):
        return self.announcement_date <= timezone.now()

class BuzzView(models.Model):
    buzz = models.ForeignKey('Buzz')
    viewer = models.ForeignKey(User)
    on_date = models.DateTimeField(auto_now_add=True, verbose_name=u"البداية")
    off_date = models.DateTimeField(null=True, blank=True, verbose_name=u"النهاية")
