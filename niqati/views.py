# -*- coding: utf-8  -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
# from django.db.models import Q
from django.core.exceptions import PermissionDenied

from core.decorators import post_only
from activities.models import Activity
from activities.forms import EvaluationForm
from niqati.models import Niqati_User, Category, Code, Code_Order, Code_Collection
from niqati.forms import OrderForm


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

# TODO: implement activity evaluation!
@login_required
def submit(request, code=""):  # (1) Shows submit code page & (2) Handles code submission requests
    if request.method == "POST":
        # format code first i.e. make upper case & remove spaces or dashes
        code = request.POST['code'].upper().replace(" ", "").replace("-", "")

        try:  # assume at first that code exists
            c = Code.objects.get(code_string=code)
            if not c.user:  # code isn't associated with any user -- free to use
                try:  # assume user already has a code in the same activity
                    a = request.user.code_set.get(activity=c.activity)
                    if c.category.points > a.category.points:  # new code has more points than existing one
                        # replace old code & show message that it has been replaced
                        a.user = None
                        a.date_redeemed = None
                        a.save()
                        c.user = request.user
                        c.date_redeemed = timezone.now()
                        c.save()
                        message_type = "-info"
                        message = u"تم إدخال الرمز بنجاح و استبدال الرمز السابق لك في هذا النشاط."
                    else:  # new code has equal or less points than existing one
                        # show message: you have codes in the same activity
                        message_type = None
                        message = u"لا يمكن إدخال هذا الرمز؛ لديك رمز نقاطي آخر في نفس النشاط ذو قيمة مساوية أو أكبر."
                except (KeyError, Code.DoesNotExist):  # no codes in the same activity
                    # redeem & show success message --- default behavior
                    c.user = request.user
                    c.date_redeemed = timezone.now()
                    c.save()
                    message_type = "-success"
                    message = u"تم تسجيل الرمز بنجاح."
            elif c.user == request.user:  # user has used the same code before
                # show message: you have used this code before
                message_type = None
                message = u"لقد استخدمت هذا الرمز من قبل؛ لا يمكنك استخدامه مرة أخرى"
            else:  # code is used by another user
                # show message: code not available (used by other)
                message_type = None
                message = u"هذا الرمز غير متوفر."
        except (KeyError, Code.DoesNotExist):  # code does not exist
            # show message: code doesn't exist
            message_type = "-error"
            message = u"هذا الرمز غير صحيح."
        return render(request, 'niqati/submit.html', {'message_type': message_type, 'message': message})
    else:  # request method is not POST
        return render(request, 'niqati/submit.html', {'code_to_redeem': code})


@login_required
def student_report(request):
    # calculate total points
    point_sum = sum(code.category.points for code in request.user.code_set.all())
    # TODO: sort codes
    return render(request, 'niqati/student_report.html', {'user': request.user, 'total_points': point_sum})


# Club Views
# TODO: reduce club coordinator views to one view, where GET requests return the order list
# and POST creates new orders

@login_required
@post_only
# @permission_required('niqati.request_order', raise_exception=True)
def create_codes(request, activity_id):
    """
    Request the creation of niqati codes.
    """
    activity = get_object_or_404(Activity, pk=activity_id)

    # --- Permission checks ---
    # The user must be the coordinator of the club that owns the activity.
    if not activity.primary_club.coordinator == request.user and not request.user.is_superuser:
        raise PermissionDenied

    form = OrderForm(request.POST)
    if form.is_valid():
        idea_c = form.cleaned_data['idea']  # idea count
        org_c = form.cleaned_data['organizer']  # org count
        par_c = form.cleaned_data['participant']  # participant count
        counts = [idea_c, org_c, par_c]
        d = form.cleaned_data['delivery_type']

        # create the Code_Order
        if idea_c > 0 or org_c > 0 or par_c > 0:  # if code count > 0
            o = Code_Order.objects.create(activity=activity)

            # create the Code_Collections
            for cat in Category.objects.all():
                if counts[cat.pk - 1] > 0:  # if ordered codes > 0
                    x = Code_Collection(code_count=counts[cat.pk - 1],
                                        code_category=cat,
                                        delivery_type=d,
                                        parent_order=o)
                    if not cat.requires_approval:  # set to approved=True if approval is not required for this category
                        x.approved = True
                    x.save()

            # create the codes
            # TODO: the url should always point to enjazportal.com. (use sites framework)
            # With this configuration, it can point to local host
            host = request.build_absolute_uri(reverse('niqati:submit'))
            print "host: " + host
            o.process(host)
            msg = u"تم إرسال الطلب؛ و سيتم إنشاء النقاط فور الموافقة عليه"
        else:
            pass
            msg = u"لم تطلب أية أكواد!"
        form = OrderForm()
    else:
        print "INvalid form"
        msg = u"الرجاء تصحيح الأخطاء أدناه"
    # return HttpResponseRedirect(reverse('activities:niqati_orders',
    #                                     args=(activity_id, )))
    return render(request, 'niqati/activity_orders.html', {'activity': activity,
                                                           'orders': activity.code_order_set.all(),
                                                           'form': form,
                                                           'msg': msg})

# --- Deprecated ---
# @login_required
# @permission_required('niqati.view_order', raise_exception=True)
# def view_orders(request):
#     activities = Activity.objects.filter(
#         Q(primary_club__coordinator=request.user),  # | Q(primary_club__members__contains=request.user),
#
#     )
#
#     context = {'activities': activities}
#     return render(request, 'niqati/orders.html', context)
# ---

@login_required
def view_orders(request, activity_id):
    """
    View niqati orders associated with a given activity.
    """
    activity = get_object_or_404(Activity, pk=activity_id)

    # --- Permission checks ---
    # Only the club coordinator has the permission to view
    # niqati orders
    if not activity.primary_club.coordinator == request.user and not request.user.is_superuser:
        raise PermissionDenied

    orders = Code_Order.objects.filter(activity=activity)
    return render(request, 'niqati/activity_orders.html', {'activity': activity,
                                                           'orders': orders,
                                                           'form': OrderForm()})

# TODO: make neater; change url name from activities:niqati_orders to activities:niqati
@login_required
def coordinator_view(request, activity_id):
    """
    If request is GET, view orders.
    If POST, create codes.
    """
    if request.method == 'POST':
        return create_codes(request, activity_id)
    else:
        return view_orders(request, activity_id)


@login_required
@permission_required('niqati.view_order', raise_exception=True)
def view_collection(request, pk):
    collec = get_object_or_404(Code_Collection, pk=pk)
    try:
        if collec.delivery_type == '0':  # Coupon
            final_file = collec.asset.read()
            response = HttpResponse(mimetype="application/pdf")
        else:  # short link
            final_file = collec.asset.read()
            response = HttpResponse(mimetype="text/html")
        response.write(final_file)
    except ValueError:  # If file doesn't exist, i.e. collection wasn't approved.
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
