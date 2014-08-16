# -*- coding: utf-8  -*-
import datetime
from django.db import models

from django.contrib.auth.models import User
from activities.models import Activity, Episode


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
    images = models.FileField(verbose_name=u"الصور", null=True, blank=True,
                              upload_to="media/images/", help_text=u"في حال وجود أكثر من صورة، يرجى رفعها كملف مضغوط.")
    notes = models.TextField(verbose_name=u"ملاحظات", null=True, blank=True)
    
    def __unicode__(self):
        "Return the name of the parent activity followed by the number of the episode"
        return self.episode.activity.name + " #" + str(list(self.episode.activity.episode_set.all()).index(self.episode) + 1)
    
    class Meta:
        permissions = (
            ("view_followupreport", "Can view a follow-up report."),
            ("view_all_followupreports", "Can view all available follow-up reports."),
        )
        verbose_name = u"تقرير"
        verbose_name_plural = u"التقارير"
#         app_label = u"المركز الإعلامي"

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
            ("assign_review_story", "Can assign any Media Center member to review a story.")
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
    date_submitted = models.DateTimeField(auto_now_add=True,
                                      verbose_name=u"تاريخ الرفع")
    
    title = models.CharField(max_length=128,
                             verbose_name=u"العنوان")
    text = models.TextField(verbose_name=u"النص")
    
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
    approve = models.BooleanField()
    
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

class TaskComment(models.Model):
    """
    Not using Django's built-in comments because we want to be able to save
    a comment and change task details at the same time. Rolling our own since it's easy.
    """
    author = models.ForeignKey(User, verbose_name=u"المعلق")
    task = models.ForeignKey(CustomTask, verbose_name=u"المهمة")
    date = models.DateTimeField(auto_now_add=True, verbose_name=u"التاريخ")
    body = models.TextField(blank=True, verbose_name=u"النص")

    def __unicode__(self):
        return '%s, %s - %s' % (
            self.task,
            self.author,
            self.date,
        )

    class Meta:
        verbose_name = u"تعليق على مهمة"
        verbose_name_plural = u"التعليقات على المهام"