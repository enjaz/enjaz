# -*- coding: utf-8  -*-
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Sum
from django.utils import timezone

from clubs.models import Club, Team
from events.managers import RegistrationQuerySet, SessionQuerySet
from ckeditor.fields import RichTextField

user_gender_choices = (
    ('F', u'طالبة'),
    ('M', u'طالب')
)

session_gender_choices = (
    ('', u'الجميع'),
    ('F', u'طالبات'),
    ('M', u'طلاب')
)

class Event(models.Model):
    official_name = models.CharField(u"الاسم الرسمي", max_length=255)
    english_name = models.CharField(u"الاسم الإنجليزي", max_length=255, default="", blank=True)

    is_official_name_english = models.BooleanField(u"هل اسم الحدث الرسمي إنجليزي", default=False)
    code_name = models.CharField(max_length=50, default="",
                                 blank=True,
                                 verbose_name=u"الاسم البرمجي",
                                 help_text=u"حروف لاتينية صغيرة وأرقام")
    registration_opening_date = models.DateTimeField(u"تاريخ فتح التسجيل", null=True, blank=True)
    registration_closing_date = models.DateTimeField(u"تاريخ انتهاء التسجيل", null=True, blank=True)
    start_date = models.DateField(u"تاريخ البدء", null=True)
    end_date = models.DateField(u"تاريخ الانتهاء", null=True)
    onsite_after = models.DateTimeField(u"التسجيل في الموقع يبدأ من", null=True, blank=True)
    url = models.URLField(max_length=255, blank=True, default="")
    location_url = models.URLField(max_length=255, blank=True, default="")
    twitter = models.CharField(max_length=255,
                               blank=True,
                               default="KSAU_Events")
    receives_abstract_submission = models.BooleanField(default=False,
                                                       verbose_name=u"يستقبل ملخصات بحثية؟")
    abstract_submission_opening_date = models.DateTimeField(u"تاريخ فتح استقبال الملخصات البحثية", null=True, blank=True)
    abstract_submission_closing_date = models.DateTimeField(u"تاريخ انتهاء إغلاق استقبال الملخصات البحثية", null=True, blank=True)
    abstract_submission_instruction_url = models.URLField(u"رابط تعليمات إرسال الأبحاث", max_length=255, blank=True, default="")
    abstract_revision_club = models.ForeignKey(Club, null=True, blank=True,
                                               related_name="abstract_revision_events")
    abstract_revision_team = models.ForeignKey(Team, null=True, blank=True,
                                               related_name="abstract_revision_events")
    is_on_telegram = models.BooleanField(default=True,
                                         verbose_name=u"على تلغرام؟")
    organizing_club = models.ForeignKey(Club , null=True)
    organizing_team = models.ForeignKey(Team, null=True)
    priorities = models.PositiveSmallIntegerField(default=1)

    def is_abstract_submission_open(self):
        #If we have abstract_submission_opening_date and/or
        # abstract_submission_closing_date, let's respect them
        if self.receives_abstract_submission and \
           (not self.abstract_submission_opening_date or \
            self.abstract_submission_opening_date and \
            timezone.now() > self.abstract_submission_opening_date) and \
           (not self.abstract_submission_closing_date or \
            self.abstract_submission_closing_date and \
            timezone.now() < self.abstract_submission_opening_date):
                return True

    def is_registration_open(self):
        #If we have registration_opening_date and/or
        # registration_closing_date, let's respect them
        if (not self.registration_opening_date or \
            self.abstract_submission_opening_date and \
            timezone.now() > self.registration_opening_date) and \
           (not self.registration_closing_date or \
            self.registration_closing_date and \
            timezone.now() < self.registration_closing_date):
            return True

    def get_html_name(self):
        if self.is_official_name_english:
            return "<span class='english-field'>" + self.official_name + "</span>"
        else:
            return self.official_name

    def get_has_multiple_sessions(self):
        """Used to generate proper emails."""
        if self.session_set.count() > 1:
            return True
        else:
            return False

    def __unicode__(self):
        return self.official_name

class TimeSlot(models.Model):
    name = models.CharField(max_length=50)
    event = models.ForeignKey(Event)
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

class Session(models.Model):
    event = models.ForeignKey(Event, null=True, blank=True)
    time_slot = models.ForeignKey(TimeSlot, default="", null=True)
    name = models.CharField(max_length=255)
    limit = models.PositiveSmallIntegerField(null=True, blank=True,
                                             default=None)
    acceptance_method_choices = (
        ('F', 'First ComeFirst Serve'),
        ('M', 'Manual')
        )
    acceptance_method = models.CharField(verbose_name="acceptance_method", max_length=1,
                                         default="", choices=acceptance_method_choices)
    description = models.TextField(blank=True, default="")
    vma_id = models.PositiveSmallIntegerField(null=True, blank=True)
    vma_time_code = models.PositiveSmallIntegerField(null=True,
                                                     blank=True,
                                                     default=None)
    code_name = models.CharField(max_length=50, default="",
                                 blank=True,
                                 verbose_name=u"الاسم البرمجي",
                                 help_text=u"حروف لاتينية صغيرة وأرقام")
    gender = models.CharField(max_length=1, blank=True,
                              default='', choices=session_gender_choices)
    location = models.CharField(blank=True, default="",
                                max_length=200,
                                verbose_name=u"المكان")
    date = models.DateField(u"التاريخ", null=True, blank=True)
    start_time = models.TimeField(u"وقت البداية", null=True, blank=True, default=None)
    end_time = models.TimeField(u"وقت النهاية", null=True, blank=True, default=None)
    date_submitted = models.DateTimeField(auto_now_add=True)
    for_onsite_registration = models.BooleanField(default=False,
                                                  verbose_name=u"متاح التسجيل في يوم الحدث؟")
    objects = SessionQuerySet.as_manager()

    def get_all_registrations(self):
        return (self.first_priority_registrations.all() | \
                self.second_priority_registrations.all()).distinct()

    def __unicode__(self):
        if self.gender:
            return u"%s (%s)" % (self.name, self.get_gender_display())
        else:
            return self.name

class NonUser(models.Model):
    ar_first_name = models.CharField(max_length=30, default="",
                                     blank=True,
                                     verbose_name=u'الاسم الأول')
    ar_middle_name = models.CharField(max_length=30, default="",
                                      blank=True,
                                      verbose_name=u'الاسم الأوسط')
    ar_last_name = models.CharField(max_length=30, default="",
                                    blank=True,
                                    verbose_name=u'الاسم الأخير')
    en_first_name = models.CharField(max_length=30,
                                     verbose_name='First name')
    en_middle_name = models.CharField(max_length=30,
                                      verbose_name='Middle name')
    en_last_name = models.CharField(max_length=30,
                                    verbose_name='Last name')
    gender = models.CharField(max_length=1, verbose_name=u'الجنس',
                              default='', choices=user_gender_choices)
    email = models.EmailField(verbose_name=u'البريد الإلكتروني')
    mobile_number = models.CharField(max_length=20,
                                     verbose_name=u'رقم الجوال')
    university = models.CharField(verbose_name=u"الجامعة", max_length=255)
    college = models.CharField(verbose_name=u"الكلية", max_length=255)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def get_ar_full_name(self):
        ar_fullname = ''
        try:
            # If the Arabic first name is missing, let's assume the
            # rest is also missing.
            if self.ar_first_name:
                ar_fullname = " ".join([self.ar_first_name,
                                     self.ar_middle_name,
                                     self.ar_last_name])
        except AttributeError: # If the user has their details missing
            pass

        return ar_fullname

    def get_en_full_name(self):
        en_fullname = ''
        try:
            # If the English first name is missing, let's assume the
            # rest is also missing.
            if self.en_first_name:
                en_fullname = " ".join([self.en_first_name,
                                     self.en_middle_name,
                                     self.en_last_name])
        except AttributeError: # If the user has their details missing
            pass

        return en_fullname

    def __unicode__(self):
        return self.get_en_full_name()

class SessionRegistration(models.Model):
    user = models.ForeignKey(User, null=True, related_name='session_registrations')
    session = models.ForeignKey(Session)
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    is_approved_choices = (
        (True, u'معتمد'),
        (False, u'مرفوض'),
        (None, u'معلق'),
        )
    is_approved = models.NullBooleanField(default= None, verbose_name=u"الحالة",
                                          choices=is_approved_choices)
    is_deleted = models.BooleanField(default=False,
                                     verbose_name=u"محذوف؟")
    reminder_sent = models.BooleanField(default=False,
                                            verbose_name=u"أرسلت رسالة التذكير؟")
    certificate_sent = models.BooleanField(default=False,
                                            verbose_name=u"أرسلت الشهادة؟")

    def __unicode__(self):
        return unicode(self.user)

class Registration(models.Model):
    user = models.ForeignKey(User, null=True, blank=True,
                             related_name='event_registrations')
    nonuser = models.ForeignKey(NonUser, null=True, blank=True,
                                related_name='event_registrations')
    first_priority_sessions  = models.ManyToManyField(Session, blank=True,
                                                      related_name="first_priority_registrations")
    second_priority_sessions  = models.ManyToManyField(Session, blank=True,
                                                      related_name="second_priority_registrations")
    moved_sessions = models.ManyToManyField(Session, blank=True,
                                            related_name="moved_registrations")
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False,
                                     verbose_name=u"محذوف؟")
    confirmation_sent = models.BooleanField(default=False,
                                            verbose_name=u"أرسلت رسالة التأكيد؟")
    reminder_sent = models.BooleanField(default=False,
                                            verbose_name=u"أرسلت رسالة التذكير؟")
    certificate_sent = models.BooleanField(default=False,
                                            verbose_name=u"أرسلت الشهادة؟")
    objects = RegistrationQuerySet.as_manager()

    def get_university(self):
        if self.user:
            try:
                common_profile = self.user.common_profile
                return "KSAU-HS"
            except ObjectDoesNotExist:
                return None
        elif self.nonuser:
            return self.nonuser.university
    get_university.short_description = u"الجامعة"

    def get_college(self):
        if self.user:
            try:
                common_profile = self.user.common_profile
                return common_profile.college.get_name_display()
            except (ObjectDoesNotExist, AttributeError):
                return None
        elif self.nonuser:
            return self.nonuser.college
    get_college.short_description = u"الكلية"

    def get_email(self):
        try:
            if self.user:
                return self.user.email
        except ObjectDoesNotExist:
            pass
        return self.nonuser.email

    def get_phone(self):
        try:
            if self.user:
                return self.user.common_profile.mobile_number
        except ObjectDoesNotExist:
            pass
        try:
            return self.nonuser.mobile_number
        except AttributeError:
            return ''

    def get_ar_first_name(self):
        if self.user:
            try:
                return self.user.common_profile.ar_first_name
            except ObjectDoesNotExist:
                return self.user.username
        elif self.nonuser:
            return self.nonuser.ar_first_name

        
    def get_ar_full_name(self):
        if self.user:
            try:
                return self.user.common_profile.get_ar_full_name()
            except ObjectDoesNotExist:
                return self.user.username
        elif self.nonuser:
            return self.nonuser.get_ar_full_name()

    def get_en_full_name(self):
        if self.user:
            try:
                return self.user.common_profile.get_en_full_name()
            except ObjectDoesNotExist:
                return self.user.username
        elif self.nonuser:
            return self.nonuser.get_en_full_name()

    def get_gender(self):
        try:
            if self.user:
                return self.user.common_profile.college.gender
        except ObjectDoesNotExist:
            pass
        try:
            return self.nonuser.gender
        except AttributeError:
            return ''
        
    def __unicode__(self):
        return self.get_en_full_name()

class Abstract(models.Model):
    user = models.ForeignKey(User, null=True, blank=True,
                             related_name='event_abstracts')
    event = models.ForeignKey(Event, verbose_name=u"الحدث")    
    title = models.CharField(verbose_name="Title", max_length=255)
    authors = models.TextField(verbose_name=u"Name of authors")
    study_field = models.CharField(verbose_name="Field", max_length=255, default="")
    university = models.CharField(verbose_name="University", max_length=255)
    college = models.CharField(verbose_name="College", max_length=255)
    presenting_author = models.CharField(verbose_name="Presenting author", max_length=255)
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(verbose_name="Phone number", max_length=20)
    level_choices = (
        ('U', 'Undergraduate'),
        ('G', 'Graduate')
        )
    level = models.CharField(verbose_name="Level", max_length=1,
                             default='', choices=level_choices)
    presentation_preference_choices = (
        ('O', 'Oral'),
        ('P', 'Poster')
        )
    presentation_preference = models.CharField(verbose_name="Presentation preference", max_length=1, choices=presentation_preference_choices)
    introduction = models.TextField(u"Introduction", default="" )
    methodology = models.TextField(u"Methodology", default="")
    results = models.TextField(u"Results", default="")
    discussion = models.TextField(u"Discussion", default="", blank=True)
    conclusion = models.TextField(u"Conclusion", default="")
    was_published = models.BooleanField(u"Have you published this research?", default=False)
    was_presented_at_others = models.BooleanField(u"Have you presented this research in any other conference before?", default=False)
    was_presented_previously = models.BooleanField(u"Have you presented this research in a previous year of this conference?", default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False,
                                     verbose_name=u"محذوف؟")

    def get_average_score(self):
        evaluation_number = self.evaluation_set.count()
        if not evaluation_number:
            return 0
        total_score = CriterionValue.objects.filter(evaluation__in=self.evaluation_set).aggregate(Sum('value'))['value__sum']
        return total_score / evaluation_number

    def __unicode__(self):
        return self.title
    
class AbstractFigure(models.Model):
    abstract = models.ForeignKey(Abstract, related_name='figures', null=True)
    figure = models.FileField(verbose_name=u"Attach the figure", upload_to="events/figures/")

class Evaluation(models.Model):
    abstract = models.ForeignKey(Abstract)
    evaluator = models.ForeignKey(User, related_name="event_abstract_evaluations")
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    def get_total_score(self):
        return self.criterion_values.aggregate(Sum('value'))['value__sum'] or 0

class Criterion(models.Model):
    event = models.ForeignKey(Event, verbose_name=u"الحدث")
    human_name = models.CharField(max_length=200,
                               verbose_name=u"اسم المعيار الذي سيظهر")
    code_name = models.CharField(max_length=200,
                                 verbose_name=u"اسم المعيار البرمجي")
    instructions = models.TextField(verbose_name=u"تعليمات")

    def __unicode__(self):
        return self.code_name

class CriterionValue(models.Model):
    evaluation = models.ForeignKey(Evaluation, verbose_name=u"التقييم",
                                   related_name="criterion_values")
    criterion = models.ForeignKey(Criterion, null=True,
                                  blank=True, on_delete=models.SET_NULL,
                                  default=None, verbose_name=u"المعيار")
    value = models.IntegerField(verbose_name=u"القيمة")

    def __unicode__(self):
        return "{}: {}".format(self.criterion.code_name, self.value)
