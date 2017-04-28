# -*- coding: utf-8  -*-
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count

from forms_builder.forms.models import Form
from core.models import StudentClubYear
from clubs.managers import ClubQuerySet, TeamQuerySet

section_choices = (
    ('NG', u'الحرس الوطني'),
    ('KF', u'مدينة الملك فهد الطبية'),
    ('J', u'جدة'),
    ('A', u'الأحساء'),
)

gender_choices = (
    ('F', u'طالبات'),
    ('M', u'طلاب'),
)

general_gender_choices = (
    ('F', u'أنثى'),
    ('M', u'ذكر'),
)

college_choices = (
    ('M', u'كلية الطب'),
    ('A', u'كلية العلوم الطبية التطبيقية'),
    ('P', u'كلية الصيدلة'),
    ('D', u'كلية طب الأسنان'),
    ('B', u'كلية العلوم و المهن الصحية'),
    ('N', u'كلية التمريض'),
    ('I', u' كلية الصحة العامة والمعلوماتية الصحية'),
)

city_choices = (
    (u'الرياض', u'الرياض'),
    (u'جدة', u'جدة'),
    (u'الأحساء', u'الأحساء'),
)

city_code_choices = (
    ('R','الرياض'),
    ('J','جدة'),
    ('A','الأحساء'))

english_city_choices = (
    (u'الرياض', u'Riyadh'),
    (u'جدة', u'Jeddah'),
    (u'الأحساء', u'Alahsa'),
)

class Club(models.Model):
    name = models.CharField(max_length=200, verbose_name=u"الاسم")
    english_name = models.CharField(max_length=200, verbose_name=u"الاسم الإنجليزي")
    description = models.TextField(verbose_name=u"الوصف", blank=True)
    logo = models.ImageField(upload_to='clubs/logos/',
                              blank=True, null=True)
    email = models.EmailField(max_length=254, verbose_name=u"البريد الإلكتروني")
    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name="children",
                               on_delete=models.SET_NULL,
                               default=None, verbose_name=u"النادي الأب")
    possible_parents = models.ManyToManyField('self',
                                              verbose_name=u"النوادي الأب الممكنة",
                                              blank=True,
                                              related_name="possible_children")
    coordinator = models.ForeignKey(User, null=True,
                                    blank=True,
                                    verbose_name=u"المنسق",
                                    related_name="coordination",
                                    on_delete=models.SET_NULL)
    deputies = models.ManyToManyField(User, verbose_name=u"النواب",
                                      blank=True,
                                      related_name="deputyships")
    media_representatives = models.ManyToManyField(User,
                                                   verbose_name=u"الممثلين ال الإعلاميين",
                                                   blank=True,
                                                   related_name="media_representations",
                                                   limit_choices_to={'common_profile__profile_type':
                                                                     'S'})
    media_assessor = models.ForeignKey(User, null=True, blank=True,
                                       related_name="media_assessments",
                                       on_delete=models.SET_NULL,
                                       default=None,
                                       verbose_name=u"المُقيّم الإعلامي",
                                       limit_choices_to={'common_profile__profile_type':
                                                         'S'})
    members = models.ManyToManyField(User, verbose_name=u"الأعضاء",
                                     blank=True,
                                     related_name="memberships")
    employee = models.ForeignKey(User, null=True, blank=True,
                                 related_name="employee",
                                 on_delete=models.SET_NULL,
                                 default=None,
                                 verbose_name=u"الموظف المسؤول",
                                 limit_choices_to={'common_profile__profile_type':
                                                   'E'})

    # To make it easy to make it specific to a certain college
    # (e.g. for membership), let's add this field.  That's also one
    # way to filter sub-clubs and college clubs.
    college = models.ForeignKey('College', null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 default=None,
                                 verbose_name=u"الكلية",)
    creation_date = models.DateTimeField(u'تاريخ الإنشاء',
                                         auto_now_add=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True)
    city = models.CharField(max_length=20, choices=city_choices, verbose_name=u"المدينة")
    gender = models.CharField(max_length=1, choices=gender_choices,
                              verbose_name=u"الجنس", blank=True,
                              default="")
    year = models.ForeignKey(StudentClubYear, null=True, blank=True,
                             on_delete=models.SET_NULL, default=None,
                             verbose_name=u"السنة")
    # Special ``Club`` objects (eg, Deanship of Student Affairs)
    # should be hidden from the clubs list
    visible = models.BooleanField(default=True,
                                  verbose_name=u"مرئي؟")
    can_review = models.BooleanField(default=False,
                                     verbose_name=u"يستطيع المراجعة؟")
    can_delete = models.BooleanField(default=True,
                                     verbose_name=u"يستطيع الحذف؟")
    can_edit = models.BooleanField(default=True,
                                     verbose_name=u"يستطيع التعديل؟")
    can_review_niqati = models.BooleanField(default=False,
                                     verbose_name=u"يستطيع مراجعة النقاط؟")
    can_assess = models.BooleanField(default=False,
                                     verbose_name=u"يستطيع تقييم لأنشطة؟")
    can_view_assessments = models.BooleanField(default=False,
                                               verbose_name=u"يستطيع مشاهدة تقييمات الأنشطة؟")
    can_skip_followup_reports = models.BooleanField(default=False,
                                                    verbose_name=u"يستطيع تجاوز التقارير الإعلامية؟")
    is_assessed =  models.BooleanField(default=True,
                                       verbose_name=u"هل يخضع للتقييم؟")
    can_submit_activities =  models.BooleanField(default=True,
                                                 verbose_name=u"هل يستطيع رفع أنشطة؟")

    forms = GenericRelation(Form)
    objects = ClubQuerySet.as_manager()

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

    def get_due_report_count(self):
        "Get the number of due follow-up reports."
        # Get all club's episodes
        episodes = []
        for activity in self.primary_activity.approved():
            episodes.extend(activity.episode_set.all())
        # Get all club's episodes whose report is due
        due_episodes = filter(lambda x: x.report_is_due() and not x.report_is_submitted(),
                              episodes)
        return len(due_episodes)
    
    def get_overdue_report_count(self):
        "Get the number of overdue follow-up reports."
        # Get all club's episodes
        episodes = []
        for activity in self.primary_activity.approved():
            episodes.extend(activity.episode_set.all())
        # Get all club's episodes whose report is overdue
        overdue_episodes = filter(lambda x: x.report_is_overdue() and not x.report_is_submitted(),
                                  episodes)
        return len(overdue_episodes)

    def get_next_activity_reviewing_parent(self):
        """
        Return the single upper parent of this club that can write activity
        reviews
        """
        current_parent = self.parent
        while current_parent:
            if current_parent.can_review:
                return current_parent
            else:
                current_parent = current_parent.parent

    def get_next_niqati_reviewing_parent(self):
        """
        Return the single upper parent of this club that can write activity
        reviews
        """
        current_parent = self.parent
        while current_parent:
            if current_parent.can_review_niqati:
                return current_parent
            else:
                current_parent = current_parent.parent

    def get_total_points(self):
        points = 0
        for primary_activity in self.primary_activity.all():
            points += primary_activity.get_presidency_assessment_points()

        secondary_points = self.secondary_activity.aggregate(secondary_points=Sum('assessment__cooperator_points'))['secondary_points']
        if secondary_points:
            points += secondary_points

        # Niqati is only included in Riyadh assessment
        if self.city == u"الرياض":
            niqati_codes =  self.primary_activity.filter(episode__order__collection__codes__user__isnull=False)\
                                                 .aggregate(count=Count('episode__order__collection__codes'))['count'] 
            if niqati_codes:
                points += niqati_codes / 10 * 2

        return points
    get_total_points.short_description = u'إجمالي النقاط'

    def get_primary_and_secondary_activities(self):
        return self.primary_activity.all() | self.secondary_activity.all()

    class Meta:
        # For the admin interface.
        verbose_name = u"نادي"
        verbose_name_plural = u"الأندية"
        permissions = (
            ("view_members", "Can view club members list."),
        )

    def __unicode__(self):
        if self.gender and not self.city:
            return u"%s (%s)" % (self.name, self.get_gender_display())
        elif self.city and not self.gender:
            return u"%s (%s)" % (self.name, self.city)
        elif self.city and self.gender:
            return u"%s (%s/%s)" % (self.name, self.city,
                                    self.get_gender_display())
        else:
            return self.name

class College(models.Model):
    section = models.CharField(max_length=2, choices=section_choices, verbose_name=u"القسم")
    name = models.CharField(max_length=1, choices=college_choices, verbose_name=u"الاسم")
    city = models.CharField(max_length=20, choices=city_choices, verbose_name=u"المدينة")
    gender = models.CharField(max_length=1, choices=gender_choices, verbose_name=u"الجنس")

    def __unicode__(self):
        return u"%s (%s - %s)" % (self.get_name_display(),
                                       self.get_section_display(),
                                       self.get_gender_display())

    class Meta:
        # For the admin interface.
        verbose_name = u"كلية"
        verbose_name_plural = u"الكليات"

class Team(models.Model):
    name = models.CharField(max_length=200, verbose_name=u"الاسم")
    code_name = models.CharField(max_length=200, verbose_name=u"الاسم البرمجي")
    email = models.EmailField(max_length=254, verbose_name=u"البريد الإلكتروني",
                              blank=True)
    year = models.ForeignKey(StudentClubYear, null=True, blank=True,
                             on_delete=models.SET_NULL, default=None,
                             verbose_name=u"السنة")
    city = models.CharField(max_length=20, choices=city_choices,
                            blank=True, default="",
                            verbose_name=u"المدينة")
    gender = models.CharField(max_length=1, choices=gender_choices,
                              verbose_name=u"الجندر", blank=True,
                              default="")
    club = models.ForeignKey(Club, null=True, blank=True,
                             verbose_name=u"النادي المتصل")
    coordinator = models.ForeignKey(User, null=True,
                                    blank=True,
                                    related_name="team_coordination",
                                    verbose_name=u"المنسق")
    members = models.ManyToManyField(User, verbose_name=u"الأعضاء",
                                     blank=True,
                                     related_name="team_memberships")
    objects = TeamQuerySet.as_manager()
    class Meta:
        # For the admin interface.
        verbose_name = u"فريق"
        verbose_name_plural = u"الفرق"

    def get_member_count(self):
        return self.members.count()

    def __unicode__(self):
        if self.gender and not self.city:
            return u"%s (%s)" % (self.name, self.get_gender_display())
        elif self.city and not self.gender:
            return u"%s (%s)" % (self.name, self.city)
        elif self.city and self.gender:
            return u"%s (%s/%s)" % (self.name, self.city,
                                    self.get_gender_display())
        else:
            return self.name
