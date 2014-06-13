# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User

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
    requirements = models.TextField(blank=True,
                                    verbose_name=u"متطلبات النشاط")
    submitter = models.ForeignKey(User, null=True,
                                  on_delete=models.SET_NULL)
    submission_date = models.DateTimeField('date submitted',
                                           auto_now_add=True)
       
#    Date,time and location are now handled by Episodes

#     location = models.CharField(max_length=200,
#                                 verbose_name=u"المكان", blank=True)
#     date = models.DateField(u'التاريخ', null=True, blank=True)
#     time = models.CharField(max_length=200, verbose_name=u'الوقت',
#                             blank=True)
#     custom_datetime = models.TextField(verbose_name=u"تاريخ ووقت مخصّص",
#                                    blank=True, help_text=u"إذا كان النشاط الذي تنوي تنظيمه دوريا أو ممتدا لفصل كامل فعبء هذه الخانة.")

    edit_date = models.DateTimeField('date edited', auto_now=True)
    is_editable = models.BooleanField(default=True)
    collect_participants = models.BooleanField(default=False,
                                               verbose_name=u"اسمح بالتسجيل؟")
    participant_colleges = models.ManyToManyField(College,
                                                  verbose_name=u"الكليات المستهدفة",
                                                  null=True, blank=True)
    inside_collaborators = models.TextField(blank=True,
                                            verbose_name=u"المتعاونون من داخل الجامعة")
    outside_collaborators = models.TextField(blank=True,
                                             verbose_name=u"المتعاونون من خارج الجامعة")
    participants = models.IntegerField(verbose_name=u"عدد المشاركين",
                                       help_text=u"العدد المتوقع للمستفيدين من النشاط")
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
            return False 
        
    def get_first_date(self):
        return self.episode_set.all()[0].start_date
        
    def get_first_time(self):
        return self.episode_set.all()[0].start_time
    
    def get_first_location(self):
        return self.episode_set.all()[0].location
    
    class Meta:
        permissions = (
            ("view_activity", "Can view all available activities."),
            ("directly_add_activity", "Can add activities directly, without approval."),
        )


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
    
    # Note: Dates and times should be interpreted as follows:
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
    
    location = models.CharField(max_length=128)
    
    # In the future, as we add Google Calendar features, the calendar events will
    # be linked here
    # google_event = models.URLField()
    
    def is_one_day(self):
        return self.start_date == self.end_date