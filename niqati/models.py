import random

from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError

from activities.models import Activity
from clubs.models import Club

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

PARTICIPANT = 'P'
ORGANIZER = 'O'
IDEA_GENERATOR = 'I'
CODE_TYPE_CHOICES = (
                     (PARTICIPANT, "Participant"),
                     (ORGANIZER, "Organizer"),
                     (IDEA_GENERATOR, "Idea Generator"),
                    )

class Code(models.Model):
    code_string = models.CharField(max_length=16, unique=True) # Each code_string is a 16-digit string, unique throughout all the db
    code_type = models.CharField(max_length=1,
                                 choices=CODE_TYPE_CHOICES)
    generation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True)
    redeem_date = models.DateTimeField(null=True, blank=True)
    # activity = models.ForeignKey(Activity) # commented out temporarily to make testing easier for a while
    # order = models.ForeignKey('Code_Order') # commented out temporarily as it is raising an Integrity error when trying to save
    
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
            
    def points(self):
        return {
                PARTICIPANT: 1,
                ORGANIZER: 2,
                IDEA_GENERATOR: 3,
                }[self.code_type]

"""
---
"""
class Code_Order(models.Model):
    COUPON = '0'
    SHORT_LINK = '1'
    ORDER_TYPE_CHOICES = (
        (COUPON, "Coupon"),
        (SHORT_LINK, "Short link"),
    )
    order_type = models.CharField(max_length=1,
                                  choices=ORDER_TYPE_CHOICES,
                                  default=COUPON)
    idea_code_count = models.IntegerField()
    organizer_code_count = models.IntegerField()
    participant_code_count = models.IntegerField()
    date_ordered = models.DateTimeField(auto_now_add=True)
    # file_path = # PDF of generated codes
    # activity = models.ForeignKey(Activity)
    
    def process(self):
        for i in range(self.idea_code_count):
            c = Code(code_type=IDEA_GENERATOR)
            c.generate_unique()
            c.save()
        for i in range(self.organizer_code_count):
            c = Code(code_type=ORGANIZER)
            c.generate_unique()
            c.save()
        for i in range(self.participant_code_count):
            c = Code(code_type=PARTICIPANT)
            c.generate_unique()
            c.save()
        """
        for code_type in CODE_TYPE_CHOICES:
            code_type = code_type[0]
            for i in range(self.ordered_code_count[code_type]):
                c = Code(code_type=code_type)
                c.generate_unique()
                c.save()
        """