# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

class Book(models.Model):
    isbn = models.CharField(max_length=13, verbose_name=u"ردمك", help_text=u"مطلوب")
    pages = models.PositiveSmallIntegerField(u"عدد الصفحات",
                                             blank=True, null=True, help_text=u"اختياري")
    title = models.CharField(max_length=200, verbose_name=u"العنوان", help_text=u"مطلوب")
    authors = models.CharField(max_length=200, verbose_name=u"تأليف", blank=True, help_text=u"اختياري")
    publisher = models.CharField(max_length=200, verbose_name=u"الناشر", blank=True, help_text=u"اختياري")
    year = models.PositiveSmallIntegerField(u"سنة النشر", null=True, blank=True, help_text=u"اختياري")
    edition = models.CharField(max_length=200, verbose_name=u"الطبعة", blank=True, help_text=u"اختياري")
    condition_choices = (
        ('Like new', u'كأنه جديد'),
        ('Very good', u'جيدة جدا'),
        ('Good', u'جيدة'),
        ('Poor', u'دون الجيدة'),
        )
    condition = models.CharField(max_length=200, verbose_name=u"حالة الكتاب",
                                 choices=condition_choices,
                                 blank=True,
                                 help_text=u"هل من صفحات ناقصة أو ممزقة مثلا؟ (اختياري)")
    description = models.TextField(verbose_name=u"وصف الكتاب", blank=True, help_text=u"اختياري")
    contact = models.CharField(max_length=200, verbose_name=u"طريقة التواصل", help_text=u"رقم جوال أو عنوان بريد (مطلوب)")
    status_choices = (
        ('A', u'متاح'),
        ('H', u'محجوز'),
        ('B', u'معار'),
        ('W', u'مسحوب'),
        ('R', u'معاد'),
        )
    status = models.CharField(max_length=1, default='A',
                              verbose_name=u"الحالة",
                              choices=status_choices)
    availability_choices = (
        ('M', u'الطلاب'),
        ('F', u'الطالبات'),
        )
    avaliable_to = models.CharField(max_length=1, verbose_name=u"متاح لقسم",
                              choices=availability_choices)
    submitter = models.ForeignKey(User, null=True,
                                  on_delete=models.SET_NULL,
                                  related_name='book_contributions')
    holder = models.ForeignKey(User, null=True,
                               on_delete=models.SET_NULL,
                               related_name='book_holdings')
    cover_url = models.CharField(max_length=200, blank=True, verbose_name=u"صورة الغلاف", help_text=u"صورة لغلاف الكتاب (مستحسن)")
    cover = models.FileField(upload_to='covers', blank=True, null=True)
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    modifiation_date = models.DateTimeField(u"تاريخ التعديل",
                                           auto_now=True)
    available_from = models.DateField(u'متوفر ابتداءً من', help_text=u"ترغب في إعارة هذا الكتاب ابتداءً من هذا التاريخ (مطلوب)")
    available_until = models.DateField(u'متوفر حتى', help_text=u"ترغب في إعارة هذا الكتاب حتى هذا التاريخ (اختياري)", null=True, blank=True)
    tags = TaggableManager(verbose_name=u"التصنيفات",
                           help_text=u"ما التصانيف الإنجليزية التي تراها ملائمة؟ (مطلوبة ومفصولة بفواصل، مثلا: \"Respiratory, Physiology\")")

    class Meta:
        permissions = (
            ('view_books', 'Can see all books regardless of their status.'),
            )

    def __unicode__(self):
        return self.title
    
class BookRequest(models.Model):
    book = models.ForeignKey(Book, null=True,
                               on_delete=models.SET_NULL)
    requester = models.ForeignKey(User, null=True,
                               on_delete=models.SET_NULL)
    status_choices = (
        ('P', u'معلقة'),
        ('W', u'ملغاة'),
        ('A', u'مقبولة'),
        ('R', u'مرفوضة'),
        ('S', u'أعيد الكتاب'),
        )
    status = models.CharField(max_length=1, default='P',
                              choices=status_choices,
                              verbose_name=u"الحالة")
    borrow_from = models.DateField(u'استعر من')
    borrow_until = models.DateField(u'استعر حتى')
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    modifiation_date = models.DateTimeField(u"تاريخ التعديل",
                                           auto_now=True)

