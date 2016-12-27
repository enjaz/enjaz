# -*- coding: utf-8  -*-
import os
from datetime import datetime, timedelta, date

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Avg, F, Sum, Count
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils import timezone

from activities.managers import ActivityQuerySet, EpisodeQuerySet
from core.models import StudentClubYear
from clubs.models import College, Club, city_choices, gender_choices
from clubs.utils import get_deanship, get_presidency
from forms_builder.forms.models import Form
from media.utils import REPORT_DUE_AFTER
import accounts.utils



class Evaluation(models.Model):
    """ An activity evaluation filled by students upon Niqati code submission. """
    episode = models.ForeignKey('Episode')
    evaluator = models.ForeignKey(User)

    # Evaluation criteria, where evaluation is on a scale from 1
    # (lowest) to 5 (highest) (So far there isn't a way to enforce min
    # and max for model fields, so this has to be done on the form
    # level)
    quality = models.PositiveIntegerField(verbose_name=u"جودة تنظيم النشاط",
                                          help_text=u"كيف تقيم عمل النادي في تنظيم النشاط؟")
    relevance = models.PositiveIntegerField(verbose_name=u"ملاءمة النشاط لاهتمام الطلاب",
                                            help_text=u"ما مدى ملاءمة النشاط لاهتمام الطلاب؟")
    class Meta:
        verbose_name = u"تقييم"
        verbose_name_plural = u"التقييمات"


class Activity(models.Model):
    primary_club = models.ForeignKey('clubs.Club', null=True,
                                     on_delete=models.SET_NULL,
                                     related_name='primary_activity',
                                     verbose_name=u"النادي المنظم")
    secondary_clubs = models.ManyToManyField('clubs.Club', blank=True,
                                            related_name="secondary_activity",
                                            verbose_name=u"الأندية المتعاونة")
    chosen_reviewer_club = models.ForeignKey('clubs.Club', null=True,
                                             blank=True,
                                             on_delete=models.SET_NULL,
                                             related_name='chosen_reviewer_activities',
                                             verbose_name=u"الكلية المراجعة")
    name = models.CharField(max_length=200, verbose_name=u"اسم النشاط")
    description = models.TextField(verbose_name=u"وصف النشاط")
    public_description = models.TextField(verbose_name=u"الوصف الإعلامي",
                                          help_text=u"هذا هو الوصف الذي سيعرض للطلاب")
    goals = models.TextField(verbose_name=u"ما أهداف هذا النشاط، وكيف يخدم المجتمع والصالح العام؟")
    requirements = models.TextField(blank=True,
                                    verbose_name=u"متطلبات النشاط الأخرى")
    submitter = models.ForeignKey(User, null=True,
                                  on_delete=models.SET_NULL)
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True)
    is_editable = models.BooleanField(default=True, verbose_name=u"هل يمكن تعديله؟")
    is_deleted = models.BooleanField(default=False, verbose_name=u"محذوف؟")
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
    forms = GenericRelation(Form)
    assignee = models.ForeignKey('clubs.Club', null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='assigned_activities',
                                 verbose_name=u"النادي المسند")
    gender_choices = (
        ('', u'الجميع'),
        ('F', u'الطالبات'),
        ('M', u'الطلاب'),
        )
    gender = models.CharField(max_length=1,verbose_name=u"النشاط موجه ل",
                              choices=gender_choices, default="",
                              blank=True)
    is_approved_choices = (
        (True, u'معتمد'),
        (False, u'مرفوض'),
        (None, u'معلق'),
        )
    is_approved = models.NullBooleanField(verbose_name=u"الحالة",
                                          choices=is_approved_choices)

    # Override the default manager with the activity custom manager
    objects = ActivityQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse("activities:show", args=(self.id, ))

    def registration_is_open(self):
        """
        Return ``True`` if there is 1 published form marked as primary. Return ``False`` if there isn't or,
        by any chance, there is more than one
        """
        return self.forms.published().filter(is_primary=True).count() == 1

    def has_registration_form(self):
        """
        A memory-efficient method to check for the presence of 1 (an only 1) primary form for a club.
        """
        return self.forms.filter(is_primary=True).count() == 1

    def get_registration_form(self):
        """
        If registration is open, return the registration form; otherwise return ``None``.
        """
        if self.has_registration_form():
            return self.forms.get(is_primary=True)
        else:
            return None

    def update_is_approved(self):
        reviewer_count = Club.objects.activity_reviewing_parents(self).count()
        # If the club has no parents, activity is approved
        # automatically
        if not self.primary_club.parent:
            self.is_approved = True

        # If all expected reviews are there, and none of them are
        # rejected or pending then consider it approved.
        elif reviewer_count <= self.review_set.count() and not \
             self.review_set.filter(models.Q(is_approved=False) |\
                                    models.Q(is_approved=None)).exists():
            self.is_approved = True

        # If there is at least one rejected review, then activity is
        # rejected
        elif self.review_set.filter(is_approved=False).exists():
            self.is_approved = False

        # In all other cases, activity is pending
        else:
            self.is_approved = None

        # REMEMBER TO SAVE AFTER YOU CALL THIS!

    def get_approval_status_message(self):
        """
        Return a verbose version of the approval status.
        """
        if self.is_approved:
            if self.assignee is None:
                return u"تمت الموافقة على النشاط."
            elif self.assignee != self.primary_club:
                return u"ينتظر تقييم %s." % self.assignee.name
        elif self.is_approved is False:
            return u"رُفض من قبل %s." % self.review_set.filter(is_approved=False).first().reviewer_club.name
        elif self.is_approved is None:
            # Either there is a pending review waiting for edits...
            if self.assignee == self.primary_club:
                return u"ينتظر تعديلاً."
            elif self.assignee:  # ... or we're waiting for the next club up the hierarchy to review activity
                return u"ينتظر مراجعة %s." % self.assignee.name
            else:
                return u"غير معروف"
    get_approval_status_message.short_description = u"حالة النشاط"

    def get_list_activity_action(self):
        """
        Return an appropriate HTML button to be displayed in the activity list based on the activity's status.
        """
        if self.is_approved is None:
            # Either there is a pending review waiting for edits...
            if self.review_set.filter(is_approved=None).exists():
                pending_reviewer = self.review_set.filter(is_approved=None).first().reviewer_club
                message = u"اقرأ مراجعة %s" % pending_reviewer.name
                url = reverse('activities:review',
                              args=(self.pk, pending_reviewer.pk))
                return "<a class='btn btn-xs btn-green' href='%s'>%s</a>" % (url, message)
            else:  # ... or we're waiting for the next club up the hierarchy to review activity
                return ""
        else:
            return ""

    def is_single_episode(self):
        return self.episode_set.count() == 1

    def get_first_date(self):
        return self.get_first_episode().start_date

    def get_first_time(self):
        return self.get_first_episode().start_time

    def get_last_date(self):
        return self.get_last_episode().end_date

    def get_last_time(self):
        return self.get_last_episode().end_time

    def get_hours(self):
        # GUESS WHAT THIS IS
        dummydate = date(2010,12,17)
        hours = 0
        for episode in self.episode_set.all():
            end = episode.end_time
            start = episode.start_time
            difference = datetime.combine(dummydate,end) - datetime.combine(dummydate,start)
            hours += abs(difference.total_seconds() /60/60)
        return int(hours)

    def get_days(self):
        days = 0
        for episode in self.episode_set.all():
            end = episode.end_date
            start = episode.start_date
            difference = (end - start).days + 1
            days += difference
        return days

    def get_codes(self):
        activity_codes = self.episode_set.filter(order__collection__codes__user__isnull=False).aggregate(count=Count('order__collection__codes'))
        return activity_codes['count']

    def get_points(self):
        return self.get_codes()/2



    def get_first_location(self):
        return self.get_first_episode()

    def get_first_episode(self):
        """
        Return the first scheduled episode for this activity.
        *** This should replace the three above-mentioned methods. ***
        """
        return self.episode_set.order_by('start_date', 'start_time').first()

    def get_last_episode(self):
        """
        Return the last scheduled episode for this activity.
        """
        return self.episode_set.order_by('-end_date', 'end_time').first()

    def get_next_episode(self):
        """
        Return the next scheduled episode for this activity.
        """
        upcoming_episodes = self.episode_set.upcoming().order_by('start_date', 'start_time')
        return upcoming_episodes.first()

    def get_next_or_last_episode(self):
        """
        Return the next scheduled episode for this activity.
        """

        upcoming_episodes = self.episode_set.upcoming().order_by('start_date', 'start_time')

        if upcoming_episodes.exists():
            return upcoming_episodes.first()
        else:
            sorted_episodes = self.episode_set.order_by('start_date', 'start_time')
            return sorted_episodes.last()

    # Evaluation-related
    def get_evaluations(self):
        """
        Get all the evaluations from all the episodes of the activity
        """
        evaluations = Evaluation.objects.filter(episode__activity=self)
        return evaluations


    def get_evaluation_count(self):
        return self.get_evaluations().count()
    get_evaluation_count.short_description = u"عدد التقييمات"

    def get_relevance_score_average(self):
        """
        Return the average evaluation score for relevance to student needs.
        """
        return self.get_evaluations().aggregate(avg=Avg('relevance'))['avg']
    get_relevance_score_average.short_description = u"معدل تقييم ملاءمة النشاط"

    def get_quality_score_average(self):
        """
        Return the average evaluation score for quality of the activity.
        """
        return self.get_evaluations().aggregate(avg=Avg('quality'))['avg']
    get_quality_score_average.short_description = u"معدل تقييم جودة النشاط"

    def get_evaluation_percentage(self):
        percentage = self.get_evaluations().aggregate(avg=Avg(F('quality') + F('relevance')))['avg']
        if percentage:
            percentage *= 10
        return percentage

    def get_presidency_assessment(self):
        return self.assessment_set.distinct().get(criterionvalue__criterion__category='P', activity=self)

    def get_media_assessment(self):
        return self.assessment_set.distinct().get(criterionvalue__criterion__category='M', activity=self)

    def get_total_assessment_points(self):
        return self.assessment_set.aggregate(total=Sum('criterionvalue__value'))['total']

    def get_presidency_assessment_points(self):
        return self.assessment_set.filter(criterionvalue__criterion__category='P').aggregate(presidency=Sum('criterionvalue__value'))['presidency']

    def get_media_assessment_points(self):
        return self.assessment_set.filter(criterionvalue__criterion__category='M').aggregate(media=Sum('criterionvalue__value'))['media']

    def get_media_assessment_points(self):
        return self.assessment_set.filter(criterionvalue__criterion__category='M').aggregate(media=Sum('criterionvalue__value'))['media']

    def get_cooperator_points(self):
        return self.assessment_set.aggregate(cooperation=Sum('cooperator_points'))['cooperation']

    def get_presidency_assessor(self):
        current_year = StudentClubYear.objects.get_current()
        # In Riyadh, there are two presidencies for each gender.
        if self.primary_club.city == 'R' and self.primary_club.gender:
            presidency_gender = self.primary_club.gender
        elif self.primary_club.city == 'R' and not self.primary_club.gender:
            # Just in case a Riyadh club doesn't have a gender fall
            # back to male presidency.
            presidency_gender = 'M'
        else: # For other cities
            presidency_gender = ''

        presidency = Club.objects.get(year=current_year,
                                        english_name__contains='Presidency',
                                        city=self.primary_club.city,
                                        gender=presidency_gender)
        return presidency

    def get_media_assessor(self):
        current_year = StudentClubYear.objects.get_current()

        # In Riyadh, there are two Media Centers for each gender.
        if self.primary_club.city == 'R' and self.primary_club.gender:
            media_center_gender = self.primary_club.gender
        elif self.primary_club.city == 'R' and not self.primary_club.gender:
            # Just in case a Riyadh club doesn't have a gender fall
            # back to male Media Center.
            media_center_gender = 'M'
        else: # For other cities
            media_center_gender = ''

        media_center = Club.objects.get(year=current_year,
                                        english_name__contains='Media Center',
                                        city=self.primary_club.city,
                                        gender=media_center_gender)
        return media_center

    def is_done(self):
        # If any episode is happening in a future date, that's enough
        # to consider the activity not done.
        future_episodes = self.episode_set.filter(end_date__gt=timezone.now().date())
        if future_episodes.exists():
            return False

        # If one of today's episode is yet to happen, consider the
        # activity not done.
        episodes_ending_today = self.episode_set.filter(end_date=timezone.now().date())
        for episode in episodes_ending_today:
            if episode.end_time > timezone.now().time():
                return False

        # Otherwise, the activity is considered done.
        return True


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
    reviewer_club = models.ForeignKey('clubs.Club', related_name="reviews",
                                      limit_choices_to={'can_review': True},
                                      verbose_name=u"النادي المراجِع",
                                      null=True)
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
    goal_notes = models.TextField(blank=True,
                                        verbose_name=u"ملاحظات على الأهداف")
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
    attachment_notes = models.TextField(blank=True,
                                             verbose_name=u"ملاحظات على المستندات المرفقة")
    submission_date_notes = models.TextField(blank=True,
                                             verbose_name=u"ملاحظات على تاريخ تقديم الطلب")
    review_type_choices = (
        ('P', u"رئاسة نادي الطلاب"),
        ('D', u"عمادة شؤون الطلاب"),
        )
    review_type = models.CharField(max_length=1, default='',
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
    ### Fields ###
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

    # Niqati-related fields
    allow_multiple_niqati = models.BooleanField(default=False, verbose_name=u"اسمح بإدخال أكثر من رمز نقاطي؟")

    # Media-related fields

    requires_report = models.BooleanField(default=True)
    can_report_early = models.BooleanField(default=False)
    requires_story = models.BooleanField(default=True)

    objects = EpisodeQuerySet.as_manager()

    ### Methods ###

    def __unicode__(self):
        return self.activity.name + " #" + str(self.get_index())

    def get_index(self):
        "Return the index (starting from 1) of the episode within the parent activity's episode set"
        return list(self.activity.episode_set.all()).index(self) + 1

    def is_single_day(self):
        return self.start_date == self.end_date

    def day_count(self):
        "Return the length of the episode in terms of days"
        return (self.end_date - self.start_date).days

    def start_datetime(self):
        return datetime.combine(self.start_date, self.start_time)

    def end_datetime(self):
        end_datetime = datetime.combine(self.end_date, self.end_time)
        if self.start_datetime() == end_datetime:
            return end_datetime + timedelta(seconds=1)
        else:
            return end_datetime

    # Evaluation-related
    # These functions are only (at least currently) to help calculate avg scores for an activity. Check ``Activity``.
    def get_relevance_score(self):
        """
        Return the average evaluation score for relevance to student needs.
        """
        relevance_scores = [e.relevance for e in self.evaluation_set.all()]
        return float(sum(relevance_scores))/len(relevance_scores) if len(relevance_scores) > 0 else 0
        # NOTE: the conditional is to avoid division by zero

    def get_quality_score(self):
        """
        Return the average evaluation score for quality of the activity.
        """
        quality_scores = [e.quality for e in self.evaluation_set.all()]
        return float(sum(quality_scores))/len(quality_scores) if len(quality_scores) > 0 else 0

    # Media-related methods

    def report_due_date(self):
        """
        Return the due date of the report, which is every Monday.
        """
        date = self.end_datetime() + timedelta(1)
        while date.weekday() != 0:
            date += timedelta(1)
        return date

    def report_is_submitted(self):
        """
        Return whether or not a report has been submitted for this episode.
        """
        try:
            report = self.followupreport
            return True
        except ObjectDoesNotExist:
            return False

    def employee_report_is_submitted(self):
        """
        Return whether or not an employee report has been submitted for this episode.
        """
        try:
            report = self.employeereport
            return True
        except ObjectDoesNotExist:
            return False

    def report_is_due(self):
        """
        Return whether the report is due.
        The report is due when the episode has ended, the due date hasn't passed,
        and the report hasn't been submitted.
        """
        return self.activity.is_approved and \
               self.requires_report and \
               self.end_datetime() < datetime.now() < self.report_due_date()

    def report_is_overdue(self):
        """
        Return whether the report is overdue.
        The report is overdue when the episode has ended, the due date has passed,
        and the report hasn't been submitted.
        """
        return self.activity.is_approved and \
               self.requires_report and \
               datetime.now() > self.report_due_date()

    def get_reviewed_niqati_orders(self):
        return self.order_set.filter(is_approved__isnull=False)

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

class Attachment(models.Model):
    activity = models.ForeignKey(Activity)
    description = models.CharField(max_length=200, verbose_name=u"الوصف", blank=True)
    preview = models.FileField(verbose_name=u"معاينة", upload_to="activity_attachment_previews/")
    document = models.FileField(verbose_name=u"المستند", upload_to="activity_attachments/")
    submitter = models.ForeignKey(User)
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)

    def filename(self):
        return os.path.basename(self.document.name)

    def __unicode__(self):
        return self.filename()

class Assessment(models.Model):
    activity = models.ForeignKey(Activity)
    assessor = models.ForeignKey(User)
    assessor_club = models.ForeignKey(Club, null=True,
                                      blank=True)
    is_reviewed = models.BooleanField(default=True, verbose_name=u"روجعت؟")
    review_date = models.DateTimeField(u'تاريخ الإرسال',
                                       null=True,
                                       blank=True)
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)
    cooperator_points = models.IntegerField(default=0,
                                            verbose_name=u"نقاط التعاون")
    notes = models.TextField(verbose_name=u"وصف النشاط", blank=True)

    def primary_points(self):
        return

class Criterion(models.Model):
    year = models.ForeignKey('core.StudentClubYear', null=True,
                             blank=True, on_delete=models.SET_NULL,
                             default=None, verbose_name=u"السنة")
    ar_name = models.CharField(max_length=200,
                               verbose_name=u"اسم المعيار بالعربية")
    code_name = models.CharField(max_length=200,
                                 verbose_name=u"اسم المعيار البرمجي")
    city = models.CharField(max_length=10, default="RAJ", verbose_name=u"المدينة")
    instructions = models.TextField(verbose_name=u"تعليمات")
    category_choices  = (
        ('P', u'رئاسة نادي الطلاب'),
        ('M', u'المركز الإعلامي')
        )
    category = models.CharField(max_length=1, verbose_name=u"التصنيف")

    def __unicode__(self):
        return self.code_name

class CriterionValue(models.Model):
    assessment = models.ForeignKey(Assessment, verbose_name=u"التقييم")
    criterion = models.ForeignKey(Criterion, null=True,
                             blank=True, on_delete=models.SET_NULL,
                             default=None, verbose_name=u"المعيار")
    value = models.IntegerField(verbose_name=u"القيمة")

    def __unicode__(self):
        return "{}: {}".format(self.criterion.code_name, self.value)

class DepositoryItem(models.Model):
    name = models.CharField(u"الاسم", default="", max_length=100)
    quantity = models.PositiveIntegerField(u"الكمية", null=True, blank=True)
    unit = models.CharField(u"الوحدة", default="", max_length=20)
    category = models.CharField(u"التصنيف", default="", max_length=40)
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True)
    def __unicode__(self):
        return self.name

class ItemRequest(models.Model):
    activity = models.ForeignKey(Activity)
    name = models.CharField(u"الاسم", default="", max_length=100)
    quantity = models.PositiveIntegerField(u"الكمية")
    unit = models.CharField(u"الوحدة", default="", max_length=20)
    category = models.CharField(u"التصنيف", default="", max_length=40)
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True)

    def __unicode__(self):
        return self.name

class Invitation(models.Model):
    title = models.CharField(u"الاسم", default="", max_length=100)
    activity = models.ForeignKey(Activity, null=True, blank=True)
    city = models.CharField(u"المدينة", max_length=1, blank=True,
                            default="", choices=city_choices)
    gender = models.CharField(u"الجندر", max_length=1,
                              choices=gender_choices, blank=True,
                              default="")
    background = models.ImageField(upload_to='invitations/backgrounds/',
                              blank=True, null=True)
    logo = models.ImageField(upload_to='invitations/logos/',
                              blank=True, null=True)
    short_description = models.TextField(u"وصف قصير")
    full_description = models.TextField(u"وصف مطول")
    twitter_account = models.CharField(u"حساب تويتر", default="",
                                       max_length=20, blank=True)
    hashtag = models.CharField(u"هاشتاغ", default="", max_length=20,
                               blank=True, help_text="بدون #")
    publication_date = models.DateTimeField(u"تاريخ النشر",
                                            blank=True, null=True)
    students = models.ManyToManyField(User, blank=True)
    location = models.CharField(u"المكان", default="",
                                max_length=200)
    date = models.DateField(u"التاريخ")
    start_time = models.TimeField(u"وقت البداية")
    end_time = models.TimeField(u"وقت النهاية")
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True)
    def is_available_for_user_city(self, user):
        user_city = accounts.utils.get_user_city(user)
        if user_city and self.city and \
           user_city != self.city:
            return False
        else:
            return True

    def is_available_for_user_gender(self, user):
        user_gender = accounts.utils.get_user_gender(user)
        if user_gender and self.gender and \
           user_gender != self.gender:
            return False
        else:
            return True

    def get_start_datetime(self):
        combined = datetime.combine(self.date, self.start_time)
        timezoned = timezone.make_aware(combined, timezone.get_default_timezone())
        return timezoned

    def get_end_datetime(self):
        combined = datetime.combine(self.date, self.end_time)
        timezoned = timezone.make_aware(combined, timezone.get_default_timezone())
        return timezoned

    def __unicode__(self):
        return self.title
