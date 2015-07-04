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

def generate_code(length):
    chars = string.ascii_uppercase + string.digits
    code = ''.join([random.choice(chars) for i in range(length)])
    return code

class Category(models.Model):
    label = models.CharField(max_length=20)
    ar_label = models.CharField(max_length=20)
    points = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.label
    
    def instructions(self):
        return {'Participation':'http://msarabi95.comyr.com/cardinstructions1pt.png',
                'Organizer':'http://msarabi95.comyr.com/cardinstructions2pt.png',
                'Idea':'http://msarabi95.comyr.com/cardinstructions3pt.png'}[self.label]

class Code(models.Model):
    # Basic Properties
    year = models.ForeignKey(StudentClubYear,
                             null=True,
                             on_delete=models.SET_NULL)
    code_string = models.CharField(max_length=16, unique=True) # a 16-digit string, unique throughout all the db
    points = models.PositiveSmallIntegerField()

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
    short_link = models.URLField(verbose_name=u"رابط قصير", null=True, blank=True)

    objects = CodeQuerySet.as_manager()
    
    # To be removed
    asset = models.CharField(max_length=300, blank=True) # either (1) short link or (2) link to QR (depending on delivery_type of parent collection)
    
    def __unicode__(self):
        return self.code_string

    def is_redeemed(self):
        return self.user is not None
    is_redeemed.boolean = True
    is_redeemed.short_description = u"تم استخدامه؟"
    
    def generate_unique(self):
        if not self.code_string: # only works when there is no string (when code is created for first time)
            while True:
                new_code = generate_code(6)
                if not Code.objects.filter(code_string=new_code).exists():
                    self.code_string = new_code
                    return
    # Obsolete.  We don't need this method anymore.  It is only kept
    # for backward compatibility.
    # returns a "spaced code" i.e. XXXX XXXX XXXX XXXX instead of XXXXXXXXXXXXXXXX
    def spaced_code(self):
        spaced_code = ""
        for i in range(len(self.code_string)):
            if i % 4 == 0 and i > 0:
                spaced_code += " "
            spaced_code += self.code_string[i]
        return spaced_code
    
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

    COUPON = '0'
    SHORT_LINK = '1'
    DELIVERY_TYPE_CHOICES = (
        (COUPON, u"كوبونات"),
        (SHORT_LINK, u"روابط قصيرة"),
    )

    # Generation-related
    code_category = models.ForeignKey(Category)
    code_count = models.PositiveSmallIntegerField()
    parent_order = models.ForeignKey('Code_Order') # --- relation to activity is through the Code_Order
    # Approval choices:
    #   None: Unreviewed
    #   True: Approved
    #   False: Rejected
    approved = models.NullBooleanField(default=None) # for idea codes

    # Delivery-related
    delivery_type = models.CharField(max_length=1, choices=DELIVERY_TYPE_CHOICES)
    date_downloaded = models.DateTimeField(null=True, blank=True, verbose_name=u"تاريخ التنزيل")

    # To be removed:
    asset = models.FileField(upload_to='niqati/codes/') # either the PDF file for coupons or the list of short links (as txt/html?)

    def __unicode__(self):
        return self.parent_order.episode.__unicode__() + " - " + self.code_category.ar_label
    
    def admin_asset_link(self):
        if self.pk:
            link = reverse('niqati:view_collec', args=(self.pk, ))
            return "<a href='%s'>%s</a>" % (link, u"اعرض الملف المرفق")
    admin_asset_link.allow_tags = True
                
    class Meta:
        verbose_name = u"مجموعة نقاط"
        verbose_name_plural = u"مجموعات النقاط"

class Code_Order(models.Model): # consists of one Code_Collection or more
    episode = models.ForeignKey(Episode, verbose_name=u"الموعد")
    date_ordered = models.DateTimeField(auto_now_add=True)
    submitter = models.ForeignKey(User, null=True,
                                  on_delete=models.SET_NULL,
                                  related_name="submitted_code")
    date_reviewed = models.DateTimeField(null=True, blank=True,
                                         verbose_name=u"تاريخ المراجعة")
    reviewer_club = models.ForeignKey('clubs.Club', related_name="reviewed_niqati_orders",
                                      limit_choices_to={'can_review_niqati': True},
                                      verbose_name=u"النادي المراجِع",
                                      null=True)
    reviewer = models.ForeignKey(User, null=True,
                                 on_delete=models.SET_NULL,
                                 related_name="reviewed_code")

    def process(self, host):
        for collec in self.code_collection_set.all():
            collec.process(host)
        self.save()

        # Send email notification after code generation
        email_context = {'order': self}
        mail.send(get_club_notification_to(self.episode.activity),
                  cc=get_club_notification_cc(self.episode.activity),
                  template="niqati_order_approve",
                  context=email_context)
    
    def is_reviewed(self):
        if len(self.code_collection_set.filter(approved=None)) == 0:
            return True
        else:
            return False

    def get_delivery_type(self):
        # This is a dirty hack, should be fixed later
        return self.code_collection_set.first().delivery_type

    def is_approved(self):
        # Might be a dirty hack as well
        return all([collec.approved for collec in self.code_collection_set.all()])

    def is_processed(self):
        return all([collec.date_created is not None for collec in self.code_collection_set.all()])

    def mark_as_processed(self):
        """
        Mark the code collections constituting the current order as processed.
        This is to prevent troublesome orders from causing delays in the generation queue.
        """
        for collec in self.code_collection_set.all():
            if collec.date_created is None:
                collec.date_created = timezone.now()
                collec.save()

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
