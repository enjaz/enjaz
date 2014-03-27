from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django import forms
from django.forms import ModelForm
from django.utils import timezone

from activities.models import Activity
from niqati.models import Category, Code, Code_Order, Code_Collection

class Order_Form(ModelForm):
    class Meta:
        model = Code_Order
        fields = ['activity']
    
    idea = forms.IntegerField()
    organizer = forms.IntegerField()
    participant = forms.IntegerField()
    delivery_type = forms.ChoiceField(choices=Code_Collection.DELIVERY_TYPE_CHOICES)

def index(request):
    return HttpResponseRedirect(reverse('niqati:submit')) 

# Student Views
@login_required
def submit(request, code=""): # (1) Shows submit code page & (2) Handles code submission requests
    if request.method == "POST":
        try: # assume at first that code exists
            c = Code.objects.get(code_string=request.POST['code'])
            if not c.user: # code isn't associated with any user -- free to use
                try: # assume user already has a code in the same activity
                    a = request.user.code_set.get(activity=c.activity)
                    if c.points() > a.points(): # new code has more points than existing one 
                        # replace old code & show message that it has been replaced
                        a.user = None
                        a.save()
                        c.user = request.user
                        c.save()
                        return render(request, 'niqati/submit.html', {
                            'message_type': "-info",
                            'message': "Success: You already have a code in this activity \
                            it has been replaced, however, by the one you just submitted.",
                        })
                    else: # new code has equal or less points than existing one
                        # show message: you have codes in the same activity
                        return render(request, 'niqati/submit.html', {
                            'message': "Can't use code: You already have a code in this activity \
                            which has equal or less value than the one you just submitted.",
                        })
                except (KeyError, Code.DoesNotExist): # no codes in the same activity
                    # redeem & show success message --- default behavior
                    c.user = request.user
                    c.save()
                    return render(request, 'niqati/submit.html', {
                        'message_type': "-success",
                        'message': "Success: This code is now part of your record.",
                    })
            elif c.user == request.user: # user has used the same code before
                # show message: you have used this code before
                return render(request, 'niqati/submit.html', {
                        'message': "Can't use code again: You have already used this code before.",
                    })
            else: # code is used by another user
                # show message: code not available (used by other)
                return render(request, 'niqati/submit.html', {
                        'message': "Can't use code: This code is already used by another person.",
                    })
        except (KeyError, Code.DoesNotExist): # code does not exist
            # show message: code doesn't exist
            return render(request, 'niqati/submit.html', {
                        'message_type': "-error",
                        'message': "Wrong code: Please verify that you entered the code correctly.",
                    })
    else: # request method is not POST
        return render(request, 'niqati/submit.html', {'code_to_redeem': code})

def student_report(request):
    return HttpResponse("This is your report: ...")

# Club Views

def create_codes(request):
    if request.method == 'POST':
        form = Order_Form(request.POST)
        if form.is_valid():
            # create the Code_Order
            
            o = Code_Order(activity=form.cleaned_data['activity'])
            o.save()            
            
            # create the Code_Collections
            
            idea_c = form.cleaned_data['idea'] # idea count
            org_c = form.cleaned_data['organizer'] # org count
            par_c = form.cleaned_data['participant'] # participant count
            
            counts = [idea_c, org_c, par_c]
            
            d = form.cleaned_data['delivery_type']
            
            for cat in Category.objects.all():
                x = Code_Collection(code_count=counts[cat.pk-1],
                                    code_category=cat,
                                    delivery_type=d,
                                    parent_order=o)
                if not cat.requires_approval: # set to approved=True if approval is not required for this category
                    x.approved = True
                x.save()
            o.save()
            
            # create the Codes
            
            for collec in o.code_collection_set.all():
                # if collec.approved:
                for i in range(collec.code_count):
                    c = Code(collection=collec,
                             activity=o.activity,
                             category=collec.code_category)
                    c.generate_unique()
                    c.save()
            
            # ---
            form = Order_Form()
            msg = "Codes created"
        else: # i.e. form.is_valid() == False
            msg = "Please correct the issues below"
            
        
        context = {'form': form, 'msg': msg}
        return render(request, 'niqati/create.html', context) 
    else:
        
        form = Order_Form()
        context = {'form': form}
        return render(request, 'niqati/create.html', context) 

def view_orders(request):
    return HttpResponse("You have ordered lots of codes.")

# Management Views

def approve_codes(request):
    return HttpResponse("No idea requests up to the moment. Enjoy your day!")

def general_report(request):
    return HttpResponse("Here is a report of all students")