from django.test import TestCase

from niqati.models import Category, Code, Code_Collection, Code_Order
from clubs.models import Club
from activities.models import Activity
"""
def db_setup():
    c = Club()
    c.name = "AAAAAAA CLUB"
    c.english_name = "ENGLISH NAME"
    c.description = "MY veRy Beautiful deScription"
    c.email = "aaa@aaa.aaa"
    c.save()
    
    a = Activity()
    a.primary_club = c
    a.name = "My Beautiful Activity"
    a.description = "My Beautiful Description"
    a.participants = 10
    a.organizers = 1
    a.save()
    return a # return activity

class Code_Create_Tests(TestCase):
    
    def test_create_codes(self):
        a = db_setup()
        orig_code_count = len(Code.objects.all())
        print "Original Code Count: %s" % orig_code_count
        o = Code_Order(activity=a)
        o.save()
        
        # create the Code_Collections
        for cat in CODE_CATEGORIES:
            collec = Code_Collection(parent_order=o,
                                     activity=o.activity,
                                     code_category=cat,
                                     code_count=1,
                                     delivery_type='0')
            collec.save()
        o.save()
        o.process()
        current_code_count = len(Code.objects.all())
        print "Current Code Count: %s" % current_code_count
        self.assertGreater(current_code_count, orig_code_count)
"""