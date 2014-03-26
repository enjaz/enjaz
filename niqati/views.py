from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.forms import ModelForm
from django.utils import timezone

from activities.models import Activity
from niqati.models import Category, Code, Code_Order, Code_Collection

class Order_Form(ModelForm):
    class Meta:
        model = Code_Order
        fields = ['activity']
        
class Collection_Form(ModelForm):
    class Meta:
        model = Code_Collection
        fields = ['code_count', 'delivery_type']

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
        r = request.POST
        print r
        form_data = {'activity': r['activity'][0]}
        form = Order_Form(form_data)
                        
        print form.is_valid()
        if form.is_valid():
            # create the Code_Order
            form.save()
            o = Code_Order.objects.get(pk=form_data['activity'])
            print o.pk
            for cat in Category.objects.all():
                subform_data = {'code_count': r['code_count'],
                                'delivery_type': r['delivery_type']
                                }
                print "subform data"
                print subform_data
                subform = Collection_Form(subform_data)
                print "subform validation"
                print subform.is_valid()
                if subform.is_valid():
                    subform['parent_order'] = o
                    subform['code_category'] = cat
                    if not cat.requires_approval:
                        subform['approved'] = True
                    subform.save()
            o.save()
            print "hello"
                
        
        return render(request, 'niqati/create.html') 
    else:
        order_form = Order_Form()
        subforms = []
        for cat in Category.objects.all():
            subforms.append(Collection_Form())
        
        context = {'order_form': order_form, 'subforms': subforms}
        return render(request, 'niqati/create.html', context) 

def view_orders(request):
    return HttpResponse("You have ordered lots of codes.")

# Management Views

def approve_codes(request):
    return HttpResponse("No idea requests up to the moment. Enjoy your day!")

def general_report(request):
    return HttpResponse("Here is a report of all students")