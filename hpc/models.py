# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User

from clubs.models import College

gender_choices = (
    ('F', 'طالبة'),
    ('M', 'طالب')
)


default_choices = [(i, i) for i in range(1, 6)]

class Abstract(models.Model):
    title = models.CharField(verbose_name="Title", max_length=255)
    authors = models.TextField(verbose_name=u"Name of authors")
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
    attachment = models.FileField(verbose_name=u"Attach the abstract", upload_to="hpc/abstract/")
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False,
                                     verbose_name=u"محذوف؟")

    def __unicode__(self):
        return self.title

class Evaluation(models.Model):
    abstract = models.OneToOneField(Abstract)
    evaluator = models.ForeignKey(User, related_name="abstract_evaluations")
    date_submitted = models.DateTimeField(auto_now_add=True)
    clear_objectives = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Is the research Objective(s) clear?")
    informative_abstract = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Is title of the ABSTRACT informative!")
    introduction = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Does the introduction cover the topic of interest!")
    clear_method = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Is the method informative and clear!")
    good_statistics = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Are the statistical methods used well described and appropriate for the purpose of the study?")
    clear_sampling = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Is the sampling technique clear and suitable to the study?")
    clear_results = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Does the result section match the methods done? Is there a result for all methods described?")
    clear_discussion = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="Is the discussion clear and answers the research question?")
    good_english = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="What is your evaluation of the English language of this paper!")
    overall_evaluation = models.PositiveSmallIntegerField(
        choices=default_choices,
        verbose_name="What is your overall evaluation of this paper?")

    def get_total_score(self):
        total_score = sum([self.clear_objectives,
                           self.informative_abstract,
                           self.introduction, self.clear_method,
                           self.good_statistics, self.clear_sampling,
                           self.clear_results, self.clear_discussion,
                           self.good_english,
                           self.overall_evaluation])
        return total_score


class Session(models.Model):
    limit = models.PositiveSmallIntegerField(null=True,
                                             default=None)
    name = models.CharField(max_length=255)
    time_slot = models.PositiveSmallIntegerField(null=True,
                                                 default=None)
    vma_id = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=1,
                              default='', choices=gender_choices)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class NonUser(models.Model):
    ar_name = models.CharField(max_length=255,
                               verbose_name=u'الاسم العربي')
    en_name = models.CharField(max_length=255,
                               verbose_name=u'الاسم الإنجليزي')
    gender = models.CharField(max_length=1, verbose_name=u'الجنس',
                              default='', choices=gender_choices)
    email = models.EmailField(verbose_name=u'البريد الإلكتروني')
    mobile_number = models.CharField(max_length=20,
                                     verbose_name=u'رقم الجوال')
    university = models.CharField(verbose_name=u"الجامعة", max_length=255)
    college = models.CharField(verbose_name=u"الكلية", max_length=255)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.ar_name

class Registration(models.Model):
    user = models.OneToOneField(User, null=True, blank=True,
                                related_name='hpc2016_registration')
    nonuser = models.OneToOneField(NonUser, null=True, blank=True,
                                    related_name='hpc2016_registration')
    sessions  = models.ManyToManyField(Session, blank=True)


    def __unicode__(self):
        if self.user:
            return self.user.common_profile.get_ar_full_name()
        elif self.nonuser:
            return self.nonuser.ar_name
        else:
            self.pk
