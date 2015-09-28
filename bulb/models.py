# -*- coding: utf-8  -*-
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User

from core.models import StudentClubYear
from bulb.managers import BookQuerySet, RequestQuerySet, PointQuerySet


class Category(models.Model):
    name = models.CharField(max_length=50,
                               verbose_name=u"اسم التصنيف")
    code_name = models.CharField(max_length=50,
                                 verbose_name=u"الاسم البرمجي",
                                 help_text=u"حروف لاتينية صغيرة وأرقام")
    description = models.TextField(blank=True, verbose_name=u"وصف التصنيف")
    image = models.FileField(upload_to='bulb/categories/', blank=True, null=True)
    def __unicode__(self):
        return self.name

class Book(models.Model):
    year = models.ForeignKey('core.StudentClubYear', null=True,
                             on_delete=models.SET_NULL)
    pages = models.PositiveSmallIntegerField(u"عدد الصفحات",
                                             blank=True, null=True, help_text=u"اختياري")
    title = models.CharField(max_length=200, verbose_name=u"العنوان")
    authors = models.CharField(max_length=200, verbose_name=u"المؤلف")
    edition = models.CharField(max_length=200, verbose_name=u"الطبعة",
                               blank=True, help_text=u"اختياري")
    condition_choices = (
        ('N', u'كأنه جديد'),
        ('VG', u'جيدة جدا'),
        ('G', u'جيدة'),
        ('P', u'دون الجيدة'),
        )
    condition = models.CharField(max_length=2, verbose_name=u"حالة الكتاب",
                                 choices=condition_choices,
                                 help_text=u"هل من صفحات ناقصة أو ممزقة مثلا؟ (اختياري)")
    description = models.TextField(verbose_name=u"وصف الكتاب", help_text=u"اختياري")
    submitter = models.ForeignKey(User,
                                  related_name='book_giveaways')
    cover = models.FileField(u"الغلاف", upload_to='bulb/covers/')
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    modifiation_date = models.DateTimeField(u"تاريخ التعديل",
                                           auto_now=True)
    category = models.ForeignKey(Category,
                                 verbose_name=u"التصنيفات",
                                 null=True,
                                 on_delete=models.SET_NULL)
    is_available = models.BooleanField(default=True,
                                       verbose_name=u"متاح؟")
    is_deleted = models.BooleanField(default=False,
                                     verbose_name=u"محذوف؟")
    objects = BookQuerySet.as_manager()


    def last_pending_request(self):
        pending_requests = self.request_set.filter(owner_status__in=['', 'F']).order_by('-submission_date')
        if pending_requests.exists():
            return pending_requests.first()

    def __unicode__(self):
        return self.title

class Request(models.Model):
    book = models.ForeignKey(Book, null=True,
                             on_delete=models.SET_NULL)
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    requester = models.ForeignKey(User)
    delivery_choices = (
        ('D', u'إيصال مباشر'),
        ('I', u'إيصال غير مباشر'),
        )
    delivery = models.CharField(max_length=1, verbose_name=u"نوع التسليم",
                                choices=delivery_choices)
    status_choices = (
        ('D', u'تم'),
        ('F', u'تعذّر'),
        ('C', u'ملغى')
        )
    requester_status = models.CharField(max_length=1, verbose_name=u"نوع التسليم",
                                        choices=status_choices, default="",
                                        blank=True)
    requester_status_date = models.DateTimeField(u"تاريخ تأكيد مقدم الطلب",
                                             blank=True, default=None,
                                             null=True)
    owner_status = models.CharField(max_length=1, verbose_name=u"نوع التسليم",
                                    choices=status_choices, default="",
                                    blank=True)
    owner_status_date = models.DateTimeField(u"تاريخ تأكيد صاحب الكتاب",
                                             blank=True, default=None,
                                             null=True)
    objects = RequestQuerySet.as_manager()

    def get_expected_delivery_date(self):
        return self.submission_date + timedelta(7)

    def get_cancellation_date(self):
        return (self.submission_date + timedelta(10)).date()

    def cancel_related_user_point(self, user):
        point = Point.objects.filter(request=self,
                                     user=user,
                                     is_counted=True)\
                             .update(is_counted=False)

    def create_related_points(self):
        current_year = StudentClubYear.objects.get_current()
        owner_points = Point.objects.filter(request=self,
                                            user=self.book.submitter,
                                            is_counted=True)
        if not owner_points.exists():
            Point.objects.create(year=current_year,
                                 request=self,
                                 user=self.book.submitter,
                                 value=1)
        requester_points = Point.objects.filter(request=self,
                                                user=self.requester,
                                                is_counted=True)
        if not requester_points.exists():
            Point.objects.create(year=current_year,
                                 request=self,
                                 user=self.requester,
                                 value=-1)

    def __unicode__(self):
        return self.book.title

class Point(models.Model):
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    year = models.ForeignKey('core.StudentClubYear', null=True,
                             on_delete=models.SET_NULL,
                             verbose_name=u"السنة")
    request = models.ForeignKey(Request, null=True, blank=True,
                                verbose_name=u"الطلب")
    user = models.ForeignKey(User, verbose_name=u"المستخدم",
                             related_name="book_points")
    is_counted = models.BooleanField(u"محسوبة؟", default=True)
    note = models.CharField(u"ملاحظة", max_length=50,
                            blank=True, default="")
    value = models.IntegerField(u"القيمة")

    objects = PointQuerySet.as_manager()

    def get_details(self):
        if self.request and self.user == self.request.requester:
            return u"طلبت الكتاب"
        elif self.request and self.user == self.request.book.submitter:
            return u"ساهمت بالكتاب."
        else:
            return self.note

    def __unicode__(self):
        return "%s (%s)" % (self.user.username, self.value)
