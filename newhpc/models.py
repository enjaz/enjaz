# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User

# blog post in arabic and english for media center to be shown at /blog
class BlogPostArabic(models.Model):
    author = models.ForeignKey(User, related_name="arabic_post_author")
    date_submitted = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=400)
    summary = models.TextField(verbose_name="240 character summary")
    text = models.TextField()
    image = models.ImageField(upload_to='hpc/blog/arabic', blank=True, null=True)
    def __unicode__(self):
        return self.title

class BlogPostEnglish(models.Model):
    author = models.ForeignKey(User, related_name="english_post_author")
    date_submitted = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=400)
    summary = models.TextField(verbose_name="240 character summary")
    text = models.TextField()
    image = models.ImageField(upload_to='hpc/blog/english', blank=True, null=True)
    def __unicode__(self):
        return self.title

#FAQ Questions and answers en/faq or ar/faq
class FaqCategory(models.Model):
    arabic_title = models.CharField(max_length=255, null=True,verbose_name="اسم التصنيف باللغة العربيّة")
    english_title = models.CharField(max_length=255,null=True,verbose_name="اسم التصنيف باللغة الانجليزيّة")
    def __unicode__(self):
        return self.english_title
class FaqQuestion(models.Model):
    category = models.ForeignKey(FaqCategory, related_name="faq_category", verbose_name="اختر تصنيف السؤال")
    is_tech = models.BooleanField(default=False,verbose_name="هل السؤال تقني ؟")
    arabic_question = models.TextField(null=True,verbose_name="السؤال باللغة العربيّة")
    english_question = models.TextField(null=True,verbose_name="السؤال باللغة الانجليزيّة")
    arabic_answer = models.TextField(null=True,verbose_name="الجواب باللغة العربيّة")
    english_answer = models.TextField(null=True,verbose_name="الجواب باللغة الانجليزيّة")
    def __unicode__(self):
        return self.english_question


# Information regarding previous editions of HPC to be shown at /previous
class PreviousVersion(models.Model):
    arabic_title = models.CharField(max_length=255, null=True, verbose_name="اسم النسخة باللغة العربيّة")
    english_title = models.CharField(max_length=255, null=True, verbose_name="اسم النسخة باللغة الانجليزيّة")
    arabic_vision = models.TextField(null=True, verbose_name="الرؤية باللغة العربيّة")
    english_vision = models.TextField(null=True, verbose_name="الرؤية باللغة الانجليزيّة")
    def __unicode__(self):
        return self.english_title

class HpcLeader(models.Model):
    version = models.ForeignKey(PreviousVersion)
    arabic_name = models.CharField(max_length=255,null=True)
    english_name = models.CharField(max_length=255,null=True)
    image = models.ImageField(upload_to='hpc/previous/HpcLeader', blank=True, null=True)
    def __unicode__(self):
        return self.english_name
class PreviousStatistics(models.Model):
    version = models.ForeignKey(PreviousVersion)
    arabic_name = models.CharField(max_length=255,null=True)
    english_name = models.CharField(max_length=255, null=True)
    number_of_attendee = models.IntegerField()
    number_of_workshops = models.IntegerField()
    number_of_speakers = models.IntegerField()
    number_of_abstracts = models.IntegerField()
    number_of_accepted_abstracts = models.IntegerField()
    number_of_universities = models.IntegerField()
    number_of_signs = models.IntegerField()
    def __unicode__(self):
        return self.english_name
class MediaSponser(models.Model):
    version = models.ForeignKey(PreviousVersion)
    arabic_name = models.CharField(max_length=255,null=True,verbose_name="الاسم باللغة العربيّة")
    english_name = models.CharField(max_length=255,null=True,verbose_name="الاسم باللغة الانجليزيّة")
    logo = models.ImageField(upload_to='hpc/previous/media', blank=True, null=True)
    def __unicode__(self):
        return self.english_name
class Winner(models.Model):
    version = models.ForeignKey(PreviousVersion)
    arabic_name = models.CharField(max_length=255,null=True,verbose_name="الاسم باللغة العربيّة")
    english_name = models.CharField(max_length=255,null=True,verbose_name="الاسم باللغة الانجليزيّة")
    arabic_description = models.TextField(null=True)
    english_description = models.TextField(null=True)
    image = models.ImageField(upload_to='hpc/previous/winner/', blank=True, null=True)
    def __unicode__(self):
        return self.english_name