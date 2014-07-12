# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from clubs.models import College

class Activity(models.Model):
    # For now, we will follow the current practice: only one club will
    # be considered the primary orginzier.  Others will be cosidered
    # secondary.
    #clubs = models.ManyToManyField('clubs.Club',
    #                               verbose_name=u"النوادي")
    primary_club = models.ForeignKey('clubs.Club', null=True,
                                     on_delete=models.SET_NULL,
                                     related_name='primary_activity',
                                     verbose_name=u"النادي المنظم")
    secondary_clubs = models.ManyToManyField('clubs.Club', blank=True,
                                            null=True,
                                            related_name="secondary_activity",
                                            verbose_name=u"الأندية المتعاونة")
    name = models.CharField(max_length=200, verbose_name=u"اسم النشاط")
    description = models.TextField(verbose_name=u"وصف النشاط")
    public_description = models.TextField(verbose_name=u"الوصف الإعلامي",
                                          help_text=u"هذا هو الوصف الذي سيعرض للطلاب")
    requirements = models.TextField(blank=True,
                                    verbose_name=u"متطلبات النشاط")
    submitter = models.ForeignKey(User, null=True,
                                  on_delete=models.SET_NULL)
    submission_date = models.DateTimeField('date submitted',
                                           auto_now_add=True)
    edit_date = models.DateTimeField('date edited', auto_now=True)
    is_editable = models.BooleanField(default=True, verbose_name=u"هل يمكن تعديله؟")
    collect_participants = models.BooleanField(default=False,
                                               verbose_name=u"افتح التسجيل للمنظمين؟")
    participant_colleges = models.ManyToManyField(College,
                                                  verbose_name=u"الكليات المستهدفة",
                                                  null=True, blank=True)
    inside_collaborators = models.TextField(blank=True,
                                            verbose_name=u"المتعاونون من داخل الجامعة")
    outside_collaborators = models.TextField(blank=True,
                                             verbose_name=u"المتعاونون من خارج الجامعة")
    participants = models.IntegerField(verbose_name=u"عدد المشاركين",
                                       help_text=u"العدد المتوقع للمستفيدين من النشاط")
    category = models.ForeignKey('Category', null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name=u"التصنيف",
                                 # If they category has sub-categories, don't show it.
                                 limit_choices_to={'category__isnull': True})
    organizers = models.IntegerField(verbose_name=u"عدد المنظمين",
                                       help_text=u"عدد الطلاب الذين سينظمون النشاط")
    
    def is_approved(self):
        try:
            d_review = self.review_set.get(review_type='D')
            if d_review.is_approved:
                return True
            else:
                return False
        except (KeyError, Review.DoesNotExist): # deanship review does not exist
            return None 
    
    def is_single_episode(self):
        return self.episode_set.count() == 1
    
    def get_first_date(self):
        return self.episode_set.all()[0].start_date # NOTE: This is not accurate as the
                                                    # first episode in the queryset may
                                                    # or may not be the first in terms
                                                    # of date and time.
                                                    # [Saeed, 4 Jul 2014]
        
    def get_first_time(self):
        return self.episode_set.all()[0].start_time
    
    def get_first_location(self):
        return self.episode_set.all()[0].location
    
    def get_first_episode(self):
        """
        Return the first scheduled episode for this activity.
        *** This should replace the three above-mentioned methods. ***
        """
        pass
    
    def get_next_episode(self):
        """
        Return the next scheduled episode for this activity.
        """
        pass
    
    class Meta:
        permissions = (
            ("view_activity", "Can view all available activities."),
            ("directly_add_activity", "Can add activities directly, without approval."),
        )
        # For the admin interface.
        verbose_name = u"نشاط"
        verbose_name_plural = u"النشاطات"

    def __unicode__(self):
        return self.name

class Review(models.Model):
    activity = models.ForeignKey(Activity, verbose_name=u" النشاط")
    reviewer = models.ForeignKey(User, null=True,
                                 on_delete=models.SET_NULL)
    review_date = models.DateTimeField(u'تاريخ المراجعة', auto_now_add=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True,
                                     null=True)
    clubs_notes = models.TextField(blank=True,
                                   verbose_name=u"ملاحظات على الأندية")
    name_notes = models.TextField(blank=True,
                                  verbose_name=u"ملاحظات على الاسم")
    datetime_notes = models.TextField(blank=True,
                                  verbose_name=u"ملاحظات على التاريخ والوقت")
    description_notes = models.TextField(blank=True,
                                        verbose_name=u"ملاحظات على الوصف")
    requirement_notes = models.TextField(blank=True,
                                        verbose_name=u"ملاحظات على المتطلبات")
    inside_notes = models.TextField(blank=True,
                                            verbose_name=u"ملاحظات المتعاونون من داخل الجامعة")
    outside_notes = models.TextField(blank=True,
                                             verbose_name=u"ملاحظات المتعاونون من خارج الجامعة")
    participants_notes = models.TextField(blank=True,
                                            verbose_name=u"ملاحظات على عدد المشاركين")
    organizers_notes = models.TextField(blank=True,
                                        verbose_name=u"ملاحظات على عدد المنظمين")
    submission_date_notes = models.TextField(blank=True,
                                             verbose_name=u"ملاحظات على تاريخ تقديم الطلب")
    review_type_choices = (
        ('P', u"رئاسة نادي الطلاب"),
        ('D', u"عمادة شؤون الطلاب"),
        )
    review_type = models.CharField(max_length=1, default='P',
                                   choices=review_type_choices,
                                   verbose_name=u"نوع المراجعة")
    approval_choices = (
        (None, u"أبقِ معلقًا"),
        (True, u"اقبل"),
        (False, u"ارفض"),
        )
    is_approved = models.NullBooleanField(choices=approval_choices,
                                          verbose_name=u"الحالة")

    class Meta:
        permissions = (
            ("view_review", "Can view all available reviews."),
            ("add_deanship_review", "Can add a review in the name of the deanship."),
            ("add_presidency_review", "Can add a review in the name of the presidency."),
            ("view_deanship_review", "Can view a review in the name of the deanship."),
            ("view_presidency_review", "Can view a review in the name of the presidency."),
        )
        # For the admin interface.
        verbose_name = u"مراجعة"
        verbose_name_plural = u"المراجعات"

    def __unicode__(self):
        return str(self.id)


class Participation(models.Model):
    activity = models.ForeignKey(Activity, verbose_name=u"النشاط")
    user = models.ForeignKey(User, null=True,
                             on_delete=models.SET_NULL)
    submission_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ("view_participation", "Can view all available participations."),
        )
        # For the admin interface.
        verbose_name = u"مشاركة"
        verbose_name_plural = u"المشاركات"

class Episode(models.Model):
    """
    Enjaz activities are usually simple a date + a start and end time. Yet this is not always the case;
    some activities have several dates and times yet all under the same activity and same request.
    Enabling the coordinators to manually enter their custom dates has a big drawback in that these custom
    dates can't be translated into something the computer can understand.
    
    Therefore, we define the "episode" model, which would be a representation of a single "unit" of
    an activity. The Activity model is related to the Episode model via a foreign key relationship. Most
    activities, however, will only require one episode, as they only consist of a single date and time.
    The more complex activites are what really take advantage of this system.
    """
    activity = models.ForeignKey(Activity)
    
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Note #1: Dates and times should be interpreted as follows:
    # start_date and end_date indicate the dates on which the episode starts and ends, respectively
    # start_time and end_time indicate the start and finish times ON EACH OF THE DATES, rather
    # than for the whole episode
    # 
    # For example:
    # start_date = yesterday, end_date = tomorrow,
    # start_time = 4:00P.M., end_time = 10:00P.M.
    # doesn't mean the episode started yesterday 4:00P.M. and ends tomorrow 10:00P.M.
    # Rather, the episode started yesterday 4:00P.M. and ended 10:00P.M., then starts today
    # 4:00P.M. and ends 10:00P.M., and the same thing for tomorrow.
    # 
    # Of course there is nothing by design to enforce this interpretation, but that's how
    # it's meant to be
    
    # Note #2: When reading the dates as strings, especially for use with the neon calendar,
    # make sure you format them in the ISO 8601 format. This is done easily by calling
    # [date_object].isoformat() (e.g. self.start_date.isoformat())
    
    location = models.CharField(max_length=128)
    
    # In the future, as we add Google Calendar features, the calendar events will
    # be linked here
    # google_event = models.URLField()
    
    def is_single_day(self):
        return self.start_date == self.end_date
    
    def day_count(self):
        "Return the length of the episode in terms of days"
        return (self.end_date - self.start_date).days
    
    def start_datetime(self):
        return datetime.combine(self.start_date, self.start_time)
    
    def end_datetime(self):
        return datetime.combine(self.end_date, self.end_time)
    
    # Media-related methods
    REPORT_DUE_AFTER = 7 # in days
    
    def report_due_date(self):
        """
        Return the due date of the report, which is within 7
        days of the end of the corresponding episode.
        """
        return self.end_datetime() + timedelta(days=self.REPORT_DUE_AFTER)
    
    def report_is_due(self):
        """
        Return whether the report is due, i.e. the episode has ended and the due date hasn't passed
        """
        return self.end_datetime() < datetime.now() < self.report_due_date()
    
    def report_is_overdue(self):
        "Return whether the report is overdue"
        return datetime.now() > self.report_due_date()

class Category(models.Model):
    ar_name = models.CharField(max_length=50,
                               verbose_name=u"اسم التصنيف")
    en_name = models.CharField(max_length=50,
                               verbose_name=u"اسم الإنجليزي")
    description = models.TextField(blank=True, verbose_name=u"وصف التصنيف")
    parent = models.ForeignKey('self', verbose_name=u"التصنيف الأب",
                               null=True, blank=True,
                               on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.ar_name


    class Meta:
        # For the admin interface.
        verbose_name = u"تصنيف"
        verbose_name_plural = u"التصنيفات"
