# -*- coding: utf-8  -*-
import string
import random
from django.core.urlresolvers import reverse
import requests
import os

from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.http import urlquote
from django.template.loader import render_to_string
from django.core.files import File
from django.conf import settings
from activities.utils import get_club_notification_to, get_club_notification_cc
from post_office import mail
from activities.models import Activity, Episode
from clubs.models import Club
from core.models import StudentClubYear
from niqati.managers import CodeQuerySet

CODE_STRING_LENGTH = 6
COUPON = '0'
SHORT_LINK = '1'

class Category(models.Model):
    label = models.CharField(max_length=20)
    ar_label = models.CharField(max_length=20)
    points = models.PositiveSmallIntegerField()
    direct_entry = models.BooleanField(default=False)

    def __unicode__(self):
        return self.label
    

class Code(models.Model):
    # Basic Properties
    year = models.ForeignKey(StudentClubYear,
                             null=True,
                             on_delete=models.SET_NULL)
    code_string = models.CharField(max_length=16, unique=True) # a 16-digit string, unique throughout all the db
    points = models.PositiveSmallIntegerField(default=0)

    # To document the reason for manually-added codes.
    note = models.CharField(max_length=200, blank=True)

    # Obsolete
    category = models.ForeignKey(Category, null=True, blank=True)

    # Generation-related
    collection = models.ForeignKey('Code_Collection', null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    generation_date = models.DateTimeField(auto_now_add=True)

    # Redeem-related
    user = models.ForeignKey(User, null=True, blank=True)
    redeem_date = models.DateTimeField(null=True, blank=True,
                                       verbose_name=u"تاريخ الإدخال")

    # to avoid generating a new link with each download, we'll store
    # the link in our db; no need to do the same for QRs.
    short_link = models.URLField(verbose_name=u"رابط قصير", blank=True, default="")

    objects = CodeQuerySet.as_manager()
    
    # Obsolete
    asset = models.CharField(max_length=300, blank=True) # either (1) short link or (2) link to QR (depending on delivery_type of parent collection)
        
    def __unicode__(self):
        return self.code_string

    def is_redeemed(self):
        return self.user is not None
    is_redeemed.boolean = True
    is_redeemed.short_description = u"تم استخدامه؟"
        
    class Meta:
        verbose_name = u"نقطة"
        verbose_name_plural = u"النقاط"
        permissions = (
            ("submit_code", "Can submit a code."),
            ("view_student_report", "Can view a report of own's codes."),
            ("view_general_report", "Can view a report of all students."),
        )
    


# When a club requests codes for a certain activity, a Code_Order is created. This Code_Order contains several
# Code_Collections, each corresponding to a code category (idea, organizer, etc.). Each Code_Collection contains all information
# and methods for creation of codes of its specific category. The Code_Order just houses the different Code_Collections
# together.
# ---
# Code_Collection is the "functional unit" of the code generation process
# Code_Order is a container that contains all Code_Collections of a single order
# ---
# Management approves idea Code_Collections, not Code_Orders
# For each activity, Clubs see a list of Code_Orders, with each containing files (e.g. PDFs) representing the Code_Collections


class Code_Collection(models.Model): # group of codes that are (1) of the same type & (2) of the same Code_Order
    # Generation-related
    code_category = models.ForeignKey(Category)
    code_count = models.PositiveSmallIntegerField()
    parent_order = models.ForeignKey('Code_Order') # --- relation to activity is through the Code_Order
    students = models.ManyToManyField(User, blank=True,
                                      limit_choices_to={'common_profile__is_student': True,
                                                        'coordination__isnull': True})

    # Approval choices:
    #   None: Unreviewed
    #   True: Approved
    #   False: Rejected
    # Obsolete
    approved = models.NullBooleanField(default=None) # for idea codes

    date_downloaded = models.DateTimeField(null=True, blank=True, verbose_name=u"تاريخ التنزيل")

    # Obsolete
    asset = models.FileField(upload_to='niqati/codes/') # either the PDF file for coupons or the list of short links (as txt/html?)

    def __unicode__(self):
        return self.parent_order.episode.__unicode__() + " - " + self.code_category.ar_label
    
    def admin_coupon_link(self):
        if self.pk:
            link = reverse('niqati:download_coupons', args=(self.pk,))
            return "<a href='%s'>%s</a>" % (link, u"اعرض الكوبونات")
    admin_coupon_link.allow_tags = True
                
    class Meta:
        verbose_name = u"مجموعة نقاط"
        verbose_name_plural = u"مجموعات النقاط"

class Code_Order(models.Model): # consists of one Code_Collection or more
    episode = models.ForeignKey(Episode, verbose_name=u"الموعد")
    date_ordered = models.DateTimeField(auto_now_add=True)
    assignee = models.ForeignKey('clubs.Club', null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='assigned_niqati_orders',
                                 verbose_name=u"النادي المسند")
    submitter = models.ForeignKey(User, null=True,
                                  on_delete=models.SET_NULL,
                                  related_name="submitted_code")

    # Approval choices:
    #   None: Unreviewed
    #   True: Approved
    #   False: Rejected
    is_approved = models.NullBooleanField(default=None)

    # Obsolete
    def is_reviewed(self):
        if len(self.code_collection_set.filter(approved=None)) == 0:
            return True
        else:
            return False

    # Obsolete (=unused)
    def get_categories(self):
        """
        Iterate over the categories includes in this order.
        Yield a queryset for each category including the codes within this order that are of that category.
        """
        for category in Category.objects.all():
            if self.codes.filter(category=category).exists():
                yield self.codes.filter(category=category)
        
    def create_codes(self):
        # To reduce database queries and to improve performance, we
        # are going to generate all random strings once and check them
        # all in one query to see if any of them is already taken.  If
        # any of them is, we would simply replace that and try again
        # until none is taken.  Previously, the number of queires was:
        #     2 * number_of_codes
        # Now, it can be as low as 2 queries for the whole collection.
        # Previously, it took 30 seconds to generate 200 codes, now it
        # takes 1 second.
        look_alike = "O0I1"
        all_chars = string.ascii_uppercase + string.digits
        chars = "".join([char for char in all_chars
                         if not char in look_alike])
        year = StudentClubYear.objects.get_current()

        for collection in self.code_collection_set.all():
            random_strings = []
            points = collection.code_category.points
            codes = []

            if collection.students.exists():
                required_codes = collection.students.count()
            else:
                required_codes = collection.code_count

            while True:
                for i in range(required_codes):
                    random_string = ''.join(random.choice(chars) for i in range(CODE_STRING_LENGTH))
                    random_strings.append(random_string)

                identical_codes = Code.objects.filter(code_string__in=random_strings)
                if identical_codes.exists():
                    identical_strings = [identical_code.code_string \
                                         for identical_code in identical_codes]
                    for identical_string in identical_strings:
                        random_strings.pop(identical_string)
                    required_codes = len(identical_strings)    
                else:
                    break
            
            # If we are deadling with direct entry of students
            if collection.students.exists():
                string_count = 0
                for student in collection.students.all():
                    random_string = random_strings[string_count]
                    codes.append(Code(code_string=random_string,
                                      points=points,
                                      collection=collection,
                                      year=year,
                                      user=student,
                                      redeem_date=timezone.now()))
                    string_count += 1
            else: # If we are deadling with counts
                    for random_string in random_strings:
                        codes.append(Code(code_string=random_string,
                                          points=points,
                                          collection=collection,
                                          year=year))
            Code.objects.bulk_create(codes)

    def __unicode__(self):
        return self.episode.__unicode__()

    class Meta:
        permissions = (
            ("request_order", "Can place a request for a code order."),
            ("view_order", "Can view existing code orders."),
            ("approve_order", "Can approve order requests."),
        )
        verbose_name = u"طلب نقاط"
        verbose_name_plural = u"طلبات النقاط"

class Review(models.Model):
    date_reviewed = models.DateTimeField(null=True, blank=True,
                                         verbose_name=u"تاريخ المراجعة",
                                         auto_now_add=True)
    reviewer_club = models.ForeignKey('clubs.Club', related_name="reviewed_niqati_orders",
                                      limit_choices_to={'can_review_niqati': True},
                                      verbose_name=u"النادي المراجِع",
                                      null=True)
    reviewer = models.ForeignKey(User, null=True,
                                 on_delete=models.SET_NULL,
                                 related_name="reviewed_niqati_orders")
    order = models.ForeignKey('Code_Order', null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    # Approval choices:
    #   None: Unreviewed
    #   True: Approved
    #   False: Rejected
    is_approved = models.NullBooleanField(default=None) # for idea codes
