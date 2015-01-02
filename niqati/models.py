# -*- coding: utf-8  -*-
import string
import random
from django.core.urlresolvers import reverse
import requests
import os
import pdfcrowd

from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.http import urlquote
from django.template.loader import render_to_string
from django.core.files import File
from django.conf import settings

from post_office import mail
from activities.models import Activity, Episode
from clubs.models import Club

def generate_code(length):
    chars = string.ascii_uppercase + string.digits
    code = ''
    for i in range(length):
        # select a random char
        char = random.choice(chars)
        code += char
    return code

class Niqati_User(User):
    def total_points(self):
        return sum(code.category.points for code in self.code_set.all())
    class Meta:
        proxy=True # nice trick to add custom methods to the User class; proxy=True means this model will use
                   # the User table and will not have a table of its own in the db

class Category(models.Model):
    label = models.CharField(max_length=20)
    ar_label = models.CharField(max_length=20)
    points = models.IntegerField()
    requires_approval = models.BooleanField(default=False)

    def __unicode__(self):
        return self.label
    
    def instructions(self):
        return {'Participation':'http://msarabi95.comyr.com/cardinstructions1pt.png',
                'Organizer':'http://msarabi95.comyr.com/cardinstructions2pt.png',
                'Idea':'http://msarabi95.comyr.com/cardinstructions3pt.png'}[self.label]

class Code(models.Model):
    # Basic Properties
    code_string = models.CharField(max_length=16, unique=True) # a 16-digit string, unique throughout all the db
    category = models.ForeignKey(Category)
    activity = models.ForeignKey(Activity)
    episode = models.ForeignKey(Episode, null=True, blank=True)

    # Generation-related
    collection = models.ForeignKey('Code_Collection')
    generation_date = models.DateTimeField(auto_now_add=True)
    asset = models.CharField(max_length=300, blank=True) # either (1) short link or (2) link to QR (depending on delivery_type of parent collection)

    # Redeem-related
    user = models.ForeignKey(User, null=True, blank=True)
    redeem_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.code_string

    def generate_unique(self):
        if not self.code_string: # only works when there is no string (when code is created for first time)
            unique = False
            while unique == False:
                new_code = generate_code(16)
                unique = True
                if len(Code.objects.filter(code_string=new_code)) == 0:
                    self.code_string = new_code
                    return
                else:
                    unique = False
    
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

    # Basics
    date_ordered = models.DateTimeField(auto_now_add=True)

    # Generation-related
    code_category = models.ForeignKey(Category)
    code_count = models.IntegerField()
    parent_order = models.ForeignKey('Code_Order') # --- relation to activity is through the Code_Order

    # Approval-related
    #   Approval choices:
    #       None: Unreviewed
    #       True: Approved
    #       False: Rejected
    approved = models.NullBooleanField(default=None) # for idea codes

    # Delivery-related
    delivery_type = models.CharField(max_length=1, choices=DELIVERY_TYPE_CHOICES)
    date_created = models.DateTimeField(null=True, blank=True, default=None) # date/time of actual code generation (after approval)
    asset = models.FileField(upload_to='niqati/codes/') # either the PDF file for coupons or the list of short links (as txt/html?)
    # thought: txt or html file not for download; instead read as strings and displayed in browser

    def admin_asset_link(self):
        if self.pk:
            link = reverse('niqati:view_collec', args=(self.pk, ))
            return "<a href='%s'>%s</a>" % (link, u"اعرض الملف المرفق")
    admin_asset_link.allow_tags = True

    def __unicode__(self):
        return self.parent_order.activity.name + " - " + self.code_category.ar_label

    class Meta:
        verbose_name = u"مجموعة نقاط"
        verbose_name_plural = u"مجموعات النقاط"

    def process(self, host):
        if self.approved and (self.date_created is None):
            for i in range(self.code_count):
                c = Code(category=self.code_category,
                         activity=self.parent_order.activity,
                         collection=self)
                c.generate_unique()
                c.save()

            if self.delivery_type == self.COUPON:

                # generate QR codes for each coupon
                qr_endpoint = "http://api.qrserver.com/v1/create-qr-code/?size=180x180&data=" + host
                for code in self.code_set.all():
                    code.asset = qr_endpoint + code.code_string
                    code.save()

                # ---

                context = {'collec': self}
                html_file = render_to_string('niqati/coupons.html', context)

                try:
                    # create an API client instance
                    client = pdfcrowd.Client(settings.PDFCROWD_USERNAME, settings.PDFCROWD_KEY)

                    # convert HTML string and save the result to a file
                    output_file = open('codes_' + str(self.pk) + '.pdf', 'wb')
                    client.convertHtml(html_file.encode('utf-8'), output_file)
                    output_file = open('codes_' + str(self.pk) + '.pdf', 'r+')
                    self.asset.save(self.parent_order.activity.name + " - " + self.code_category.ar_label, File(output_file))
                    self.save()
                    
                    output_file.close()
                    os.remove('codes_' + str(self.pk) + '.pdf')

                except pdfcrowd.Error, why:
                    print 'Failed:', why
                

            else:
                # generate short links for each code
                for code in self.code_set.all():
                    long_link = urlquote(host + code.code_string)
                    response = requests.get("https://api-ssl.bitly.com/v3/shorten?access_token=" + settings.BITLY_KEY + "&format=txt&longUrl=" + long_link)
                    short_link = response.text
                    code.asset = short_link
                    code.save()
                # generate a file that houses them all
                
                context = {'collec': self}
                html_file = render_to_string('niqati/links.html', context)
                
                output_file = open('links_' + str(self.pk) + '.html', 'wb')
                output_file.write(html_file.encode('utf-16'))
                output_file = open('links_' + str(self.pk) + '.html', "r+")
                self.asset.save(self.parent_order.activity.name + " - " + self.code_category.ar_label, File(output_file))
                output_file.close()
                
                os.remove('links_' + str(self.pk) + '.html')

            # Record the date and time the collection was processed
            # Placing this at the end ensures that collections which experience issues while
            # being processed won't be falsely marked as processed
            self.date_created = timezone.now()
            self.save()
                

class Code_Order(models.Model): # consists of one Code_Collection or more
    activity = models.ForeignKey(Activity, verbose_name=u"النشاط")
    episode = models.ForeignKey(Episode, verbose_name=u"الموعد", null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def process(self, host):
        for collec in self.code_collection_set.all():
            collec.process(host)
        self.save()

        # Send email notification after code generation
        email_context = {'order': self}
        if self.episode.activity.primary_club.coordinator:
            recipient = self.episode.activity.primary_club.coordinator.email
        else:
            recipient = self.episode.activity.submitter.email
        mail.send([recipient],
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
