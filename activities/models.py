# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta

from clubs.models import College

class Activity(models.Model):
    # For now, we will follow the current practice: only one club will
    # be considered the primary orginzier.  Others will be cosidered
    # secondary.
    #clubs = models.ManyToManyField('clubs.Club',
    #                               verbose_name=u"الأندية")
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
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True)
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

    def is_approved_by_deanship(self):
        try:
            d_review = self.review_set.get(review_type='D')
            return d_review.is_approved
        except (KeyError, Review.DoesNotExist): # deanship review does not exist
            return None
    is_approved_by_deanship.boolean = True
    is_approved_by_deanship.short_description = u"اعتمدته العمادة؟"

    def is_approved_by_presidency(self):
        try:
            p_review = self.review_set.get(review_type='P')
            return p_review.is_approved
        except (KeyError, Review.DoesNotExist): # presidency review does not exist
            return None
    is_approved_by_presidency.boolean = True
    is_approved_by_presidency.short_description = u"اعتمدته الرئاسة؟"

    def is_approved(self):
        if self.get_approval_status() == 6:
            return True
        elif self.get_approval_status() == 2 or self.get_approval_status() == 5:
            return False
        else:
            return None
        # return self.is_approved_by_deanship()

    def get_approval_status(self):
        """
        Returns the approval status of the activity as a number within the range 0 to 6, where 6 is approved.
        """
        reviews = self.review_set.all()
        if not reviews.exists():
            return 0
        elif reviews.filter(review_type="P", is_approved=None).exists() and \
            not reviews.filter(review_type="D").exists():
            return 1
        elif reviews.filter(review_type="P", is_approved=False).exists() and \
            not reviews.filter(review_type="D").exists():
            return 2
        elif reviews.filter(review_type="P", is_approved=True).exists() and \
            not reviews.filter(review_type="D").exists():
            return 3
        elif reviews.filter(review_type="P", is_approved=True).exists() and \
            reviews.filter(review_type="D", is_approved=None).exists():
            return 4
        elif reviews.filter(review_type="P", is_approved=True).exists() and \
            reviews.filter(review_type="D", is_approved=False).exists():
            return 5
        elif reviews.filter(review_type="P", is_approved=True).exists() and \
            reviews.filter(review_type="D", is_approved=True).exists():
            return 6

    def get_approval_status_message(self):
        """
        Return a verbose version of the approval status.
        """
        return {0: u"لم تتم مراجعته بعد.",
                1: u"ينتظر تعديلاً.",
                2: u"رفضته رئاسة نادي الطلاب.",
                3: u"ينتظر مراجعة عمادة شؤون الطلاب.",
                4: u"ينتظر تعديلًا.",
                5: u"رفضته عمادة شؤون الطلاب.",
                6: u"تمت الموافقة على النشاط.",
                None: u"غير معروف",
                }[self.get_approval_status()]

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
        pass # TODO: implement get_first_episode
    
    def get_next_episode(self):
        """
        Return the next scheduled episode for this activity.
        """
        pass # TODO: implement get_next_episode

    # Evaluation-related
    def get_relevance_score_average(self):
        """
        Return the average evaluation score for relevance to student needs.
        """
        relevance_scores = [e.relevance for e in self.evaluation_set.all()]
        return float(sum(relevance_scores))/len(relevance_scores) if len(relevance_scores) > 0 else 0
        # NOTE: the conditional is to avoid division by zero
    get_relevance_score_average.short_description = u"معدل تقييم ملاءمة النشاط"

    def get_quality_score_average(self):
        """
        Return the average evaluation score for quality of the activity.
        """
        quality_scores = [e.quality for e in self.evaluation_set.all()]
        return float(sum(quality_scores))/len(quality_scores) if len(quality_scores) > 0 else 0
    get_quality_score_average.short_description = u"معدل تقييم جودة النشاط"

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
    
    def __unicode__(self):
        return self.activity.name + " #" + str(self.get_index() + 1)
    
    def get_index(self):
        "Return the index of the episode within the parent activity's episode set"
        return list(self.activity.episode_set.all()).index(self)
    
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
        Return whether the report is due.
        The report is due when the episode has ended, the due date hasn't passed,
        and the report hasn't been submitted.
        """
        try:
            report = self.followupreport
            report_not_submitted = False
        except ObjectDoesNotExist:
            report_not_submitted = True
        return self.end_datetime() < datetime.now() < self.report_due_date() and report_not_submitted
    
    def report_is_overdue(self):
        """
        Return whether the report is overdue.
        The report is overdue when the episode has ended, the due date has passed,
        and the report hasn't been submitted.
        """
        try:
            report = self.followupreport
            report_not_submitted = False
        except ObjectDoesNotExist:
            report_not_submitted = True
        return datetime.now() > self.report_due_date() and report_not_submitted

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


class Evaluation(models.Model):
    """ An activity evaluation filled by students upon Niqati code submission. """
    activity = models.ForeignKey(Activity)  # TODO: change to episode (when niqati.models.Code has been changed)
    evaluator = models.ForeignKey(User)

    # Evaluation criteria, where evaluation is on a scale from 1 (lowest) to 5 (highest)
    # (So far there isn't a way to enforce min and max for model fields, so this has
    # to be done on the form level)
    quality = models.PositiveIntegerField(verbose_name=u"جودة تنظيم النشاط",
                                          help_text=u"كيف تقيم عمل النادي في تنظيم النشاط؟")
    relevance = models.PositiveIntegerField(verbose_name=u"ملاءمة النشاط لاهتمام الطلاب",
                                            help_text=u"ما مدى ملاءمة النشاط لاهتمام الطلاب؟")
    class Meta:
        verbose_name = u"تقييم"
        verbose_name_plural = u"التقييمات"
