import random

from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError

from activities.models import Activity

class Code(models.Model):
    # Each code_string is a 16-digit string which is unique
    # throughout all the db
    code_string = models.CharField(max_length=16, unique=True)
#    activity = models.ForeignKey(Activity)
    generation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True)
    redeem_date = models.DateTimeField(null=True, blank=True)
    
    def __unicode__(self):
        return self.code_string
    
    # --- Override the save() function
    # This function assigns a unique string to each code before
    # saving it to the database
    # The reason this is bound to save() rather than any other function
    # is to make sure no codes exist elsewhere in the system other than the db
    # and new codes only have to be compared to one source
    def save(self, *args, **kwargs):
        duplicate_code = True # it should be false actually but the while loop won't start then
        # Keep generating codes until unique code is generated
        while duplicate_code:
            duplicate_code = False
            self.code_string = generate_code(16)
            try:
                # call original save
                super(Code, self).save(*args, **kwargs)
                break
            except IntegrityError: # This is raised when there is duplication (self.code_string has unique=True)
                duplicate_code = True
                
    
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
