# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from researchhub.managers import ResearchHubQuerySet, ProjectQuerySet


class Project(models.Model):
    year = models.ForeignKey('core.StudentClubYear', null=True,
                             on_delete=models.SET_NULL)
    field = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    submitter = models.ForeignKey(User,
                                  related_name='submitted_research_projects')
    supervisor = models.CharField(max_length=100)
    description = models.TextField("Project description",
                                   help_text="Please write in as much detail as you can.")
    required_role = models.TextField()
    prerequisites = models.TextField("Prerequisites",
                                     default="", blank=True,
                                     help_text="What kind of skills do you need in participants? (Optional)")
    duration = models.CharField(max_length=100)
    communication = models.TextField("Communication method (name/details)")
    submission_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    is_personal = models.BooleanField("Is a personal project?",
                                      default=True,
                                      help_text="Only shown to ReseachHub team members.  Check when this is the personal project of the submitter.")
    is_hidden = models.BooleanField("Is hidden?", default=False)
    is_deleted = models.BooleanField("Is deleted?", default=False)
    objects = ProjectQuerySet.as_manager()

    def __unicode__(self):
        return self.title

class Domain(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to='researchhub/domain/', blank=True)

    def __unicode__(self):
        return self.name

class Supervisor(models.Model):
    domain = models.ForeignKey(Domain, default="")

    year = models.ForeignKey('core.StudentClubYear', null=True,
                             on_delete=models.SET_NULL)
    specialty = models.CharField(max_length=100, blank=True)
    avatar = models.FileField(upload_to='researchhub/supervisors/',
                              blank=True, help_text="Optional")
    user = models.OneToOneField(User,
                                limit_choices_to={'common_profile__is_student': False})
    interests = models.TextField("Research areas of interest")
    communication = models.TextField("Communication method")
    submission_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField("Is hidden?", default=False)
    is_deleted = models.BooleanField("Is deleted?", default=False)
    available_from = models.DateField(null=True, blank=True, help_text="Optional")
    available_until = models.DateField(null=True, blank=True, help_text="Optional")
    objects = ResearchHubQuerySet.as_manager()

    def is_currently_available(self):
        if not self.is_hidden or \
           self.available_from and self.available_from > timezone.now() or \
           self.available_until and self.available_until < timezone.now():
            return False
        else:
            return True

    def __unicode__(self):
        try:
            return self.user.common_profile.get_en_full_name()
        except ObjectDoesNotExist:
            return self.user.username

class Skill(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to='researchhub/skill/', blank=True)

    def __unicode__(self):
        return self.name

class SkilledStudent(models.Model):
    skill = models.ForeignKey(Skill, default="")

    year = models.ForeignKey('core.StudentClubYear', null=True,
                             on_delete=models.SET_NULL)
    user = models.ForeignKey(User,
                             related_name="researchhub_skill_profiles")
    description = models.TextField(help_text="Describe your skills in as much detail as you can.")
    previous_experience = models.TextField(help_text="In what projects have you utilized your skills in the past?  (Optional)",
                                           blank=True)
    ongoing_projects = models.TextField(help_text="Do you have ongoing projects in which you have used these skills? (Optional)", blank=True)
    condition = models.TextField(blank=True,
                                 help_text="Do you have any conditions for joining a research project? (Optional)")
    is_hidden = models.BooleanField("Is hidden?", default=False)
    available_from = models.DateField(null=True, blank=True, help_text="Optional")
    available_until = models.DateField(null=True, blank=True,
                                       help_text="How long are you going to be available? (Optional)")
    submission_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField("Is deleted?", default=False)

    objects = ResearchHubQuerySet.as_manager()

    def is_within_availability_dates(self):
        if not self.is_hidden or \
           self.available_from and self.available_from > timezone.now() or \
           self.available_until and self.available_until < timezone.now():
            return False
        else:
            return True

    def __unicode__(self):
        try:
            return self.user.common_profile.get_en_full_name()
        except ObjectDoesNotExist:
            return self.user.username
