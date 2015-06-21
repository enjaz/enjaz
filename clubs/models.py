# -*- coding: utf-8  -*-
from django.contrib.contenttypes.generic import GenericRelation
from django.db import models
from django.contrib.auth.models import User
from forms_builder.forms.models import Form
from core.models import StudentClubYear
from clubs.managers import ClubQuerySet

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
    ('R', u'الرياض'),
    ('J', u'جدة'),
    ('A', u'الأحساء'),
)

class Club(models.Model):
    name = models.CharField(max_length=200, verbose_name=u"الاسم")
    english_name = models.CharField(max_length=200, verbose_name=u"الاسم الإنجليزي")
    description = models.TextField(verbose_name=u"الوصف", blank=True)
    email = models.EmailField(max_length=254, verbose_name=u"البريد الإلكتروني")
    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name="children",
                               on_delete=models.SET_NULL,
                               default=None, verbose_name=u"النادي الأب")
    coordinator = models.ForeignKey(User, null=True,
                                    blank=True,
                                    verbose_name=u"المنسق",
                                    related_name="coordination",
                                    on_delete=models.SET_NULL,
                                    # To exclude AnonymousUser
                                    limit_choices_to={'pk__gt': -1})
    deputies = models.ManyToManyField(User, verbose_name=u"النواب",
                                      blank=True,
                                      related_name="deputyships",
                                      limit_choices_to={'common_profile__is_student':
                                                        False})
    members = models.ManyToManyField(User, verbose_name=u"الأعضاء",
                                     blank=True,
                                     related_name="memberships",
                                     limit_choices_to={'common_profile__is_student':
                                                       False})
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
    creation_date = models.DateTimeField(u'تاريخ الإنشاء',
                                         auto_now_add=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True)
    city = models.CharField(max_length=1, choices=city_choices, verbose_name=u"المدينة")
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
        due_episodes = filter(lambda x: x.report_is_due(),
                              episodes)
        return len(due_episodes)
    
    def get_overdue_report_count(self):
        "Get the number of overdue follow-up reports."
        # Get all club's episodes
        episodes = []
        for activity in self.primary_activity.approved():
            episodes.extend(activity.episode_set.all())
        # Get all club's episodes whose report is overdue
        overdue_episodes = filter(lambda x: x.report_is_overdue(),
                                  episodes)
        return len(overdue_episodes)

    def get_next_reviewing_parent(self):
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
            return u"%s (%s)" % (self.name, self.get_city_display())
        elif self.city and self.gender:
            return u"%s (%s/%s)" % (self.name, self.get_city_display(),
                                    self.get_gender_display())
        else:
            return self.name

class College(models.Model):
    section = models.CharField(max_length=2, choices=section_choices, verbose_name=u"القسم")
    name = models.CharField(max_length=1, choices=college_choices, verbose_name=u"الاسم")
    city = models.CharField(max_length=1, choices=city_choices, verbose_name=u"المدينة")
    gender = models.CharField(max_length=1, choices=gender_choices, verbose_name=u"الجنس")

    def __unicode__(self):
        return u"%s (%s - %s)" % (self.get_name_display(),
                                       self.get_section_display(),
                                       self.get_gender_display())

    class Meta:
        # For the admin interface.
        verbose_name = u"كلية"
        verbose_name_plural = u"الكليات"
