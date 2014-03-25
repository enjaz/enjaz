from django.test import TestCase

from niqati.models import Code, Code_Order

class Code_Tests(TestCase):
    
    def test_new_code_is_unique(self):
        for i in range(100):
            c = Code()
            c.generate_unique()
            new_code = c.code_string
            all = Code.objects
            self.assertEqual(len(all.filter(code_string=new_code)), 0)
            c.save()
    
        
class Code_Order_Tests(TestCase):
    
    def test_order_process(self):
        base_code_count = len(Code.objects.all())
        o = Code_Order(idea_code_count=1, organizer_code_count=3, participant_code_count=10)
        o.process()
        new_code_count = len(Code.objects.all())
        self.assertGreater(new_code_count, base_code_count)