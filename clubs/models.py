# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User

section_choices = (
    ('M', u'طلاب'),
    ('F', u'طالبات'),
    ('KM', u'طلاب مدينة الملك فهد الطبية'),
    ('KF', u'طالبات مدينة الملك فهد الطبية'),
)
college_choices = (
    ('M', u'كلية الطب'),
    ('A', u'كلية العلوم الطبية التطبيقية'),
    ('P', u'كلية الصيدلة'),
    ('D', u'كلية طب الأسنان'),
    ('B', u'كلية العلوم و المهن الصحية'),
    ('N', u'كلية التمريض'),
)

city_choices = (
    ('R', u'الرياض'),
    ('J', u'جدة'),
    ('A', u'الأحساء'),
    )

class Club(models.Model):
    name = models.CharField(max_length=200, verbose_name=u"الاسم")
    english_name = models.CharField(max_length=200, verbose_name=u"الاسم الإنجليزي")
    description = models.TextField(verbose_name=u"الوصف")
    email = models.EmailField(max_length=254, verbose_name=u"البريد الإلكتروني")
    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name="parenthood",
                               on_delete=models.SET_NULL,
                               default=None, verbose_name=u"النادي الأب")
    coordinator = models.ForeignKey(User, null=True,
                                    blank=True,
                                    verbose_name=u"المنسق",
                                    related_name="coordination",
                                    on_delete=models.SET_NULL,
                                    # To exclude AnonymousUser
                                    limit_choices_to={'pk__gt': -1})
    members = models.ManyToManyField(User, null=True,
                                     verbose_name=u"الأعضاء",
                                     blank=True,
                                     related_name="memberships")
    employee = models.ForeignKey(User, null=True, blank=True,
                                 related_name="employee",
                                 on_delete=models.SET_NULL,
                                 default=None,
                                 verbose_name=u"الموظف المسؤول",
                                 limit_choices_to={'user_permissions__codename': 'deanship_employee'})
    # To make it easy to make it specific to a certain college
    # (e.g. for membership), let's add this field.  That's also one
    # way to filter sub-clubs and college clubs.
    college = models.ForeignKey('College', null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 default=None,
                                 verbose_name=u"الكلية",)
    open_membership = models.BooleanField(default=False,
                                               verbose_name=u"اسمح بالتسجيل؟")
    creation_date = models.DateTimeField('date created',
                                         auto_now_add=True)
    edit_date = models.DateTimeField('date edited', auto_now=True)
    special = models.BooleanField(default=False,
                                  verbose_name=u"نادي مميز؟") # To allow more flexible exceptions with
                                                         # presidency, media club and arshidny
    city = models.CharField(max_length=1, choices=city_choices, verbose_name=u"المدينة")
    def get_due_report_count(self):
        "Get the number of due follow-up reports."
        # Get all club's episodes
        episodes = []
        for activity in self.primary_activity.all():
            episodes.extend(activity.episode_set.all())
        # Get all club's episodes whose report is due
        due_episodes = filter(lambda x: x.report_is_due(),
                              episodes)
        return len(due_episodes)
    
    def get_overdue_report_count(self):
        "Get the number of overdue follow-up reports."
        # Get all club's episodes
        episodes = []
        for activity in self.primary_activity.all():
            episodes.extend(activity.episode_set.all())
        # Get all club's episodes whose report is overdue
        overdue_episodes = filter(lambda x: x.report_is_overdue(),
                                  episodes)
        return len(overdue_episodes)
        
    class Meta:
        # For the admin interface.
        verbose_name = u"نادي"
        verbose_name_plural = u"الأندية"
    def __unicode__(self):
        return self.name

class MembershipApplication(models.Model):
    club = models.ForeignKey(Club, related_name='club')
    user = models.ForeignKey(User, related_name='user')
    note = models.TextField(verbose_name=u"لماذا تريد الانضمام؟",
           help_text=u"هل لديك مهارات مخصوصة؟ هل لديك أفكار لنشاطات؟")
    submission_date = models.DateTimeField('تاريخ الإرسال',
                                           auto_now_add=True)

    class Meta:
        permissions = (
            ("view_application", "Can view all available applications."),
        )

    def __unicode__(self):
        return self.user

class College(models.Model):
    section = models.CharField(max_length=2, choices=section_choices, verbose_name=u"القسم")
    name = models.CharField(max_length=1, choices=college_choices, verbose_name=u"الاسم")
    city = models.CharField(max_length=1, choices=city_choices, verbose_name=u"المدينة")

    def __unicode__(self):
        return u"%s (%s)" % (self.get_name_display(), self.get_section_display())

    class Meta:
        # For the admin interface.
        verbose_name = u"كلية"
        verbose_name_plural = u"الكليات"

    def get_college_full_name(self):
        college_dict = dict(college_choices)
        return college_dict[self.name]

    def get_city_full_name(self):
        city_dict = dict(city_choices)
        try:
            city_full_name = city_dict[self.city]
        except KeyError: # Riyadh should be the default
            city_full_name = u"الرياض"
        return city_full_name
