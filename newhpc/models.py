from django.db import models
from django.contrib.auth.models import User

# blog post and author models
class BlogPost(models.Model):
    author = models.ForeignKey(User, related_name="post_author")
    date_submitted = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=400)
    summary = models.TextField(verbose_name="240 character summary")
    text = models.TextField()
    image = models.ImageField(upload_to='hpc/blog', blank=True, null=True)

#FAQ Questions and answers
class FaqCategory(models.Model):
    name = models.CharField(max_length=255)

class FaqQuestion(models.Model):
    category = models.ForeignKey(FaqCategory, related_name="faq_category")
    is_tech = models.BooleanField(default=False,verbose_name="Is the question technical?")
    question = models.TextField()
    answer = models.TextField()


# Previous editions of HPC
class PreviousVersion(models.Model):
    name = models.CharField(max_length=255)
    vision = models.TextField()

class HpcLeader(models.Model):
    version = models.ForeignKey(PreviousVersion)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='hpc/previous/HpcLeader', blank=True, null=True)

class PreviousStatistics(models.Model):
    version = models.ForeignKey(PreviousVersion)
    number_of_attendee = models.IntegerField()
    number_of_workshops = models.IntegerField()
    number_of_speakers = models.IntegerField()
    number_of_abstracts = models.IntegerField()
    number_of_accepted_abstracts = models.IntegerField()
    number_of_universities = models.IntegerField()
    number_of_signs = models.IntegerField()
class MediaSponser(models.Model):
    version = models.ForeignKey(PreviousVersion)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='hpc/previous/media', blank=True, null=True)
class winner(models.Model):
    version = models.ForeignKey(PreviousVersion)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='hpc/previous/winner/', blank=True, null=True)