# -*- coding: utf-8  -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django import forms
from django.forms import ModelForm
from django.utils import timezone
from django.db.models import Q

from activities.models import Activity
from niqati.models import Niqati_User, Category, Code, Code_Order, Code_Collection

class Order_Form(ModelForm):
    class Meta:
        model = Code_Order
        fields = ['activity']
    
    idea = forms.IntegerField(label=u"الفكرة", help_text=u"عدد نقاط الفكرة")
    organizer = forms.IntegerField(label=u"المنظمون", help_text=u"عدد نقاط التنظيم")
    participant = forms.IntegerField(label=u"المشاركون", help_text=u"عدد نقاط المشاركة")
    delivery_type = forms.ChoiceField(label=u"طريقة التسليم",
                      choices=Code_Collection.DELIVERY_TYPE_CHOICES)

@login_required
def index(request):
    user = request.user
    if user.has_perms('niqati.view_general_report'):
        return HttpResponseRedirect(reverse('niqati:general_report')) 
    elif user.has_perms('niqati.approve_order'):
        return HttpResponseRedirect(reverse('niqati:approve')) 
    elif user.has_perms('niqati.view_order'):
        return HttpResponseRedirect(reverse('niqati:orders')) 
    else:
        return HttpResponseRedirect(reverse('niqati:submit')) 

# Student Views
@login_required
def submit(request, code=""): # (1) Shows submit code page & (2) Handles code submission requests
    if request.method == "POST":
        # format code first i.e. make upper case & remove spaces or dashes
        code = request.POST['code'].upper().replace(" ","").replace("-","")

        try: # assume at first that code exists
            c = Code.objects.get(code_string=code)
            if not c.user: # code isn't associated with any user -- free to use
                try: # assume user already has a code in the same activity
                    a = request.user.code_set.get(activity=c.activity)
                    if c.category.points > a.category.points: # new code has more points than existing one 
                        # replace old code & show message that it has been replaced
                        a.user = None
                        a.date_redeemed = None
                        a.save()
                        c.user = request.user
                        c.date_redeemed = timezone.now()
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
                    c.date_redeemed = timezone.now()
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

@login_required
def student_report(request):
    # calculate total points
    point_sum = sum(code.category.points for code in request.user.code_set.all())
    # TODO: sort codes
    return render(request, 'niqati/student_report.html', {'user': request.user, 'total_points': point_sum})

# Club Views

@login_required
@permission_required('niqati.request_order', raise_exception=True)
def create_codes(request):
    if request.method == 'POST':
        form = Order_Form(request.POST)
        if form.is_valid():            
            idea_c = form.cleaned_data['idea'] # idea count
            org_c = form.cleaned_data['organizer'] # org count
            par_c = form.cleaned_data['participant'] # participant count
            counts = [idea_c, org_c, par_c]
            d = form.cleaned_data['delivery_type']
            
            # create the Code_Order
            if idea_c > 0 or org_c > 0 or par_c > 0: # if code count > 0
                o = Code_Order.objects.create(activity=form.cleaned_data['activity'])
                
                # create the Code_Collections
                for cat in Category.objects.all():
                    if counts[cat.pk-1] > 0: # if ordered codes > 0
                        x = Code_Collection(code_count=counts[cat.pk-1],
                                            code_category=cat,
                                            delivery_type=d,
                                            parent_order=o)
                        if not cat.requires_approval: # set to approved=True if approval is not required for this category
                            x.approved = True
                        x.save()

                # create the codes
                host = request.build_absolute_uri(reverse('niqati:submit'))
                print "host: " + host
                o.process(host)
                msg = "تم إرسال الطلب؛ و سيتم إنشاء النقاط فور الموافقة عليه."
            
            else:
                msg = u"لم تطلب أية أكواد!"
                
            form = Order_Form()
        else: # i.e. form.is_valid() == False
            msg = u"الرجاء تصحيح الأخطاء أدناه"
            
        context = {}
        context['msg'] = msg
        # return render(request, 'niqati/create.html', context) 
    else:
        form = Order_Form()
        context = {}
    
    form.fields['activity'].queryset = Activity.objects.filter(
                        Q(primary_club__coordinator=request.user), # | Q(primary_club__members__contains=request.user),
                        
                        )
    context['form'] = form
    return render(request, 'niqati/create.html', context) 

@login_required
@permission_required('niqati.view_order', raise_exception=True)
def view_orders(request):
    activities = Activity.objects.all()
    
    context = {'activities': activities}
    return render(request, 'niqati/orders.html', context)

@login_required
@permission_required('niqati.view_order', raise_exception=True)
def view_collection(request, pk):
    collec = get_object_or_404(Code_Collection, pk=pk)
    try:
        if collec.delivery_type == '0': # Coupon
            final_file = collec.asset.read()
            response = HttpResponse(mimetype="application/pdf")
        else: # short link
            final_file = collec.asset.read()
            response = HttpResponse(mimetype="text/html")
        response.write(final_file)
    except ValueError: # If file doesn't exist, i.e. collection wasn't approved.
        if collec.approved == False:
            context = {'message': 'disapproved'}
        elif collec.approved == None:
            context = {'message': 'pending'}
        else:
            context = {'message': 'unknown'}
        response = render(request, 'niqati/order_not_approved.html', context)

    return response

# Management Views

@login_required
@permission_required('niqati.approve_order', raise_exception=True)
def approve_codes(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        if request.POST['action'] == "approve_order":
            order = Code_Order.objects.get(pk=pk)
            for collec in order.code_collection_set.filter(approved=None):
                collec.approved = True
                collec.save()
            
            host = request.build_absolute_uri(reverse('niqati:submit'))
            order.process(host)
            
        elif request.POST['action'] == "reject_order":
            order = Code_Order.objects.get(pk=pk)
            for collec in order.code_collection_set.filter(approved=None):
                collec.approved = False
                collec.save()
                
        elif request.POST['action'] == "approve_collec":
            collec = Code_Collection.objects.get(pk=pk)
            collec.approved = True
            
            host = request.build_absolute_uri(reverse('niqati:submit'))
            collec.process(host)
            collec.save()
            
        elif request.POST['action'] == "reject_collec":
            collec = Code_Collection.objects.get(pk=pk)
            collec.approved = False
            collec.save()
    
    unapproved_collec = Code_Collection.objects.filter(approved=None)
    activities = []
    for collec in unapproved_collec:
        if not collec.parent_order.activity in activities:
            activities.append(collec.parent_order.activity)
    context = {'unapproved_collec': unapproved_collec, 'activities': activities}
    return render(request, 'niqati/approve.html', context)

@login_required
@permission_required('niqati.view_general_report', raise_exception=True)
def general_report(request):
    users = Niqati_User.objects.all()
    
    return render(request, 'niqati/general_report.html', {'users': users})
