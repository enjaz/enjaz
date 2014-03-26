import random

from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone

from activities.models import Activity
from clubs.models import Club

"""
def generate_code(length):
    chars = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
           'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6',
           '7', '8', '9', '0')
    code = ''
    for i in range(length):
        # select a random char
        j = random.randint(0, 35)
        code += chars[j]
    return code


#######                             vvvvv
# Must find solution to categories (below) 
#                                   vvvvv
#######

PARTICIPANT = 'P'
ORGANIZER = 'O'
IDEA_GENERATOR = 'I'
CODE_CATEGORY_CHOICES = (
                     (PARTICIPANT, "Participant"),
                     (ORGANIZER, "Organizer"),
                     (IDEA_GENERATOR, "Idea Generator"),
                    )

CODE_CATEGORIES = {
                   IDEA_GENERATOR: {'label': "Idea", 'points': 3},
                   ORGANIZER: {'label': "Organizer", 'points': 2},
                   PARTICIPANT: {'label': "Participant", 'points': 1},
                   }

#######
"""
class Category(models.Model):
    label = models.CharField(max_length=20)
    ar_label = models.CharField(max_length=20)
    points = models.IntegerField()
    requires_approval = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.label

class Code(models.Model):
    # Basic Properties
    code_string = models.CharField(max_length=16, unique=True) # a 16-digit string, unique throughout all the db
    category = models.ForeignKey(Category)
    activity = models.ForeignKey(Activity)
    
    # Generation-related
    collection = models.ForeignKey('Code_Collection')
    generation_date = models.DateTimeField(auto_now_add=True)
    
    # Redeem-related
    user = models.ForeignKey(User, null=True, blank=True)
    redeem_date = models.DateTimeField(null=True, blank=True)
    
    def __unicode__(self):
        return self.code_string
"""    
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
            
    def points(self):
        return {
                PARTICIPANT: 1,
                ORGANIZER: 2,
                IDEA_GENERATOR: 3,
                }[self.code_type]
"""

"""
When a club requests codes for a certain activity, a Code_Order is created. This Code_Order contains several
Code_Collections, each corresponding to a code category (idea, organizer, etc.). Each Code_Collection contains all information
and methods for creation of codes of its specific category. The Code_Order just houses the different Code_Collections
together.
---
Code_Collection is the "functional unit" of the code generation process
Code_Order is a container that contains all Code_Collections of a single order
---
Management approves idea Code_Collections, not Code_Orders
For each activity, Clubs see a list of Code_Orders, with each containing files (e.g. PDFs) representing the Code_Collections
"""
    
COUPON = '0'
SHORT_LINK = '1'
DELIVERY_TYPE_CHOICES = (
    (COUPON, "Coupon"),
    (SHORT_LINK, "Short link"),
)
    
class Code_Collection(models.Model): # group of codes that are (1) of the same type & (2) of the same Code_Order
    # Basics
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    # Generation-related
    code_category = models.ForeignKey(Category)
    code_count = models.IntegerField()
    parent_order = models.ForeignKey('Code_Order') # --- relation to activity is through the Code_Order
    
    # Approval-related
    approved = models.BooleanField(default=False) # for idea codes
    
    # Delivery-related
    delivery_type = models.CharField(max_length=1, choices=DELIVERY_TYPE_CHOICES)
    date_created = models.DateTimeField(null=True, blank=True) # date/time of actual code generation (after approval)
    asset = "" # either the PDF file for coupons or the list of short links (as txt/html?)
    # thought: txt or html file not for download; instead read as strings and displayed in browser
    
    """
    def process(self):
        if (not self.code_category == "I") or self.approved:
            for i in range(self.code_count):
                c = Code(code_type=self.code_category)
                c.activity = self.activity
                c.generate_unique()
                c.save()
            self.date_created = timezone.now()
    """
    
class Code_Order(models.Model): # consists of one Code_Collection or more
    activity = models.ForeignKey(Activity)
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    """
    def process(self):
        for collec in self.code_collection_set.all():
            collec.process()
    """