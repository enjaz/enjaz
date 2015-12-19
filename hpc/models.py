# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User

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
