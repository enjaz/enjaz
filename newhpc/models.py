# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User

# blog post in arabic and english for media center to be shown at /blog
class BlogPostArabic(models.Model):
    author = models.ForeignKey(User, related_name="arabic_post_author",default="")
    date_submitted = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=400,default="")
    summary = models.TextField(verbose_name="240 character summary",default="")
    text = models.TextField(default="")
    image = models.ImageField(upload_to='newhpc/blog/arabic', blank=True, null=True)
    def __unicode__(self):
        return self.title

class BlogPostEnglish(models.Model):
    author = models.ForeignKey(User, related_name="english_post_author")
    date_submitted = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=400,default="")
    summary = models.TextField(verbose_name="240 character summary",default="")
    text = models.TextField(default="")
    image = models.ImageField(upload_to='newhpc/blog/english', null=True,blank=True)
    def __unicode__(self):
        return self.title

#FAQ Questions and answers en/faq or ar/faq
class FaqCategory(models.Model):
    arabic_title = models.CharField(max_length=255, default="",verbose_name="اسم التصنيف باللغة العربيّة")
    english_title = models.CharField(max_length=255,default="",verbose_name="اسم التصنيف باللغة الانجليزيّة")
    def __unicode__(self):
        return self.english_title
class FaqQuestion(models.Model):
    category = models.ForeignKey(FaqCategory, related_name="faq_category", verbose_name="اختر تصنيف السؤال")
    is_tech = models.BooleanField(default=False,verbose_name="هل السؤال تقني ؟")
    arabic_question = models.TextField(default="",verbose_name="السؤال باللغة العربيّة")
    english_question = models.TextField(default="",verbose_name="السؤال باللغة الانجليزيّة")
    arabic_answer = models.TextField(default="",verbose_name="الجواب باللغة العربيّة")
    english_answer = models.TextField(default="",verbose_name="الجواب باللغة الانجليزيّة")
    def __unicode__(self):
        return self.english_question


# Information regarding previous editions of HPC to be shown at /previous
class PreviousVersion(models.Model):
    arabic_title = models.CharField(max_length=255, default="", verbose_name="اسم النسخة باللغة العربيّة")
    english_title = models.CharField(max_length=255,default="", verbose_name="اسم النسخة باللغة الانجليزيّة")
    arabic_vision = models.TextField(default="", blank=True,verbose_name="الرؤية باللغة العربيّة غير مطلوب")
    english_vision = models.TextField(default="", blank= True,verbose_name="الرؤية باللغة الانجليزيّة غير مطلوب")
    logo = models.ImageField(upload_to="newhpc/prevous/logo",null=True,blank=True,verbose_name="شعار النسخة")
    show_more = models.URLField(verbose_name="Gallery Show more pictures link",default="",blank=True)

    def __unicode__(self):
        return self.english_title

class Gallery(models.Model):
    version = models.ForeignKey(PreviousVersion)
    picture = models.FileField(verbose_name="Attach the picture", upload_to="newhpc/gallery/",null=True,blank=True)

class HpcLeader(models.Model):
    version = models.ForeignKey(PreviousVersion)
    arabic_name = models.CharField(max_length=255,default="")
    image = models.ImageField(upload_to='newhpc/previous/HpcLeader', blank=True, null=True,verbose_name="الصورة الشخصيّة")
    def __unicode__(self):
        return self.arabic_name

class PreviousStatistics(models.Model):
    version = models.ForeignKey(PreviousVersion)
    number_of_signs = models.IntegerField(default=0,verbose_name="عدد تسجيلات الدخول والخروج خلال أيّام المؤتمر الثلاث")
    number_of_workshops = models.IntegerField(default=0,verbose_name="عدد ورش العمل")
    number_of_lectures = models.IntegerField(default=0,verbose_name="عدد المحاضرات")
    number_of_speakers = models.IntegerField(default=0,verbose_name="عدد المتحدّثين")
    number_of_abstracts = models.IntegerField(default=0,verbose_name="عدد الأبحاث المتقدّمة")
    number_of_accepted_abstracts = models.IntegerField(default=0,verbose_name="عدد الأبحاث المقبولة")
    oral_presentations = models.IntegerField(default=0,verbose_name="العروض البحثيّة")
    poster_presentations = models.IntegerField(default=0,verbose_name="الملصقات البحثيّة")
    number_of_winners = models.IntegerField(default=0,verbose_name="عدد الفائزين بالأبحاث")
    number_of_universities = models.IntegerField(default=0,verbose_name="عدد الجامعات المشاركة")
    def __unicode__(self):
        return self.version

class Speaker(models.Model):
    version = models.ForeignKey(PreviousVersion)
    is_top_speaker = models.BooleanField(default=False,verbose_name="هل هو من المتحدّثين البارزين الذين سيتم عرضهم في الصفحة الرئيسيّة")
    name = models.CharField(max_length=255, default="",blank=True, verbose_name="اسم المتحدّث باللغة المتوفّرة")
    position = models.CharField(max_length=255, default="",blank=True, verbose_name="منصب المتحدّث مطلوب في حال كان المتحدّث بارز")
    image = models.ImageField(upload_to='newhpc/previous/speaker', blank=True, null=True,verbose_name="الصورة مطلوبة في حال كون المتحدّث بارز")
    def __unicode__(self):
        return self.name
# Winner
class Winner(models.Model):
    version = models.ForeignKey(PreviousVersion)
    arabic_name = models.CharField(max_length=255,default="",verbose_name="الاسم باللغة العربيّة")
    presentation_type_choices = (
        ('O', 'Oral'),
        ('P', 'Poster')
        )
    rank_choices = (
        ('1', 'المركز الأوّل'),
        ('2', 'المركز الثاني'),
        ('3','المركز الثالث'),
        ('4', 'المركز الرابع'),
        ('5', 'المركز الخامس'),
        ('6', 'المركز السادس'),
        ('7', 'المركز السابع'),
        ('8', 'المركز الثامن'),
        ('9', 'المركز التاسع'),
        ('10', 'المركز العاشر')
        )
    presentation_type = models.CharField(verbose_name="نوع البحث", max_length=1, choices=presentation_type_choices,default="")
    rank = models.CharField(max_length=1,choices=rank_choices,default="",verbose_name="المركز")
    image = models.ImageField(upload_to='newhpc/previous/winner/', blank=True, null=True, verbose_name="صورة الفائز غير مطلوبة في حال عدم التوفّر")
    def __unicode__(self):
        return self.arabic_name

