# -*- coding: utf-8  -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models import Sum
from django.core.exceptions import PermissionDenied

from post_office import mail
from accounts.models import get_gender
from core.decorators import post_only
from core.utilities import MVP_EMAIL, FVP_EMAIL
from activities.models import Activity, Evaluation
from activities.forms import EvaluationForm
from activities.utils import get_club_notification_to, get_club_notification_cc
from clubs.utils import has_coordination_to_activity, can_review_niqati, is_coordinator_or_deputy_of_any_club
from niqati.models import Category, Code, Code_Order, Code_Collection, COUPON, SHORT_LINK
from niqati.forms import OrderForm, RedeemCodeForm


@login_required
def index(request):
    user = request.user
    if user.has_perms('niqati.view_general_report'): # Superuser
        return HttpResponseRedirect(reverse('niqati:general_report'))
    elif can_review_niqati(user):
        return HttpResponseRedirect(reverse('niqati:approve'))
    elif is_coordinator_or_deputy_of_any_club(user):
        return HttpResponseRedirect(reverse('niqati:orders'))
    else: # Student Views
        return HttpResponseRedirect(reverse('niqati:submit'))

@login_required
def redeem(request, code=""):
    """
    GET: show the code submission form.
    POST: submit a code.
    """
    #if timezone.now() > timezone.datetime(2015, 4, 21, 0, 0, 0, tzinfo=timezone.get_default_timezone()):
    #    return render(request, "niqati/submit_closed.html")
    if request.method == "POST":
        form = RedeemCodeForm(request.user, request.POST)
        eval_form = EvaluationForm(request.POST)
        if form.is_valid() and eval_form.is_valid():
            result = form.process()
            messages.add_message(request, *result)
            eval_form.save(form.code.event, request.user)
            return HttpResponseRedirect(reverse("codes:submit"))
    elif request.method == "GET":
        form = RedeemCodeForm(request.user, initial={'string': code})
        eval_form = EvaluationForm()
    return render(request, "niqati/submit.html", {"form": form,  "eval_form": eval_form})
    
@login_required
def student_report(request):
    # calculate total points
    context = request.user.code_set.aggregate(total_points=Sum('category__points'))
    # TODO: sort codes
    return render(request, 'niqati/student_report.html', context)


# Club Views
# TODO: reduce club coordinator views to one view, where GET requests return the order list
# and POST creates new orders

@login_required
def coordinator_view(request, activity_id):
    """
    If request is GET, view orders.
    If POST, create codes.
    """

    activity = get_object_or_404(Activity, pk=activity_id)

    # --- Permission checks ---
    # Only the club coordinator has the permission to view
    # niqati orders
    if not has_coordination_to_activity(request.user, activity) \
       and not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = OrderForm(request.POST, activity=activity)
        if form.is_valid():
            episode = form.cleaned_data['episode']
            idea_count = form.cleaned_data['idea']  # idea count
            org_count = form.cleaned_data['organizer']  # org count
            par_ccount = form.cleaned_data['participant']  # participant count
            delivery_type = form.cleaned_data['delivery_type']

            labels = {
                'idea': (idea_count, Category.objects.get(label="Idea")),
                'organizer': (org_count, Category.objects.get(label="Organizer")),
                'participant': (par_ccount, Category.objects.get(label="Participation")),
                }

            for label in labels:
                count = labels[label][0]
                category = labels[label][1]
                if count: # Not zero
                    Code_Collection.objects.create(code_count=count,
                                                   code_category=category,
                                                   delivery_type=delivery_type,
                                                   parent_order=order)

                # send email to presidency for approval
                email_context = {'order': order}
                mail.send([MVP_EMAIL],
                          template="niqati_order_submit",
                          context=email_context)

                msg = u"تم إرسال الطلب؛ و سيتم إنشاء النقاط فور الموافقة عليه"
                messages.add_message(request, messages.SUCCESS, msg)
            else:
                msg = u"لم تطلب أية أكواد!"
                messages.add_message(request, messages.WARNING, msg)
        else:
            msg = u"الرجاء ملء النموذج بشكل صحيح."
            messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect(reverse("activities:niqati_orders", args=(activity.id, )))
    elif request.method == 'GET':
        return render(request, 'niqati/activity_orders.html', {'activity': activity,
                                                           'form': OrderForm(activity=activity),
                                                           'active_tab': 'niqati'})

@login_required
def download_collection(request, pk, order_id, download_type):
    collection = get_object_or_404(Code_Collection, pk=pk)
    activity = collection.parent_order.episode.activity
    domain = Site.objects.get_current().domain

    if not has_coordination_to_activity(request.user, activity) and \
       not request.user.is_superuser:
        raise PermissionDenied

    if download_type == COUPON:
        endpoint = "http://api.qrserver.com/v1/create-qr-code/?size=180x180&data=" + domain

        response = render(request, 'niqati/includes/coupons.html', {"order": order,
                                                                   "domain": domain,
                                                                   "endpoint": endpoint})
    elif download_type == SHORT_LINK:
        endpoint = "https://api-ssl.bitly.com/v3/shorten?format=txt&access_token=%(api_key)s&longUrl=" % {"api_key": settings.BITLY_KEY}

        response = render(request, 'niqati/includes/links.html', {"order": order,
                                                                 "domain": domain,
                                                                 "endpoint": endpoint})
    # Mark codes as downloaded
    collection.date_downloaded = timezone.now()

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

            # host = request.build_absolute_uri(reverse('niqati:submit'))
            # order.process(host)

        elif request.POST['action'] == "reject_order":
            order = Code_Order.objects.get(pk=pk)
            order.code_collection_set.filter(approved=None).update(approved=False)
            # Send email notification after code generation
            email_context = {'order': order}
            mail.send(get_club_notification_to(order.episode.activity),
                      cc=get_club_notification_cc(order.episode.activity),
                      template="niqati_order_reject",
                      context=email_context)

        elif request.POST['action'] == "approve_collec":
            collec = Code_Collection.objects.get(pk=pk)
            collec.approved = True

        elif request.POST['action'] == "reject_collec":
            collec = Code_Collection.objects.get(pk=pk)
            collec.approved = False
            collec.save()

        return HttpResponseRedirect(reverse("niqati:approve"))

    elif request.method == 'GET':
        unapproved_collec = Code_Collection.objects.filter(approved=None)
        activities = []
        for collec in unapproved_collec:
            if not collec.parent_order.episode.activity in activities:
                activities.append(collec.parent_order.episode.activity)
        context = {'unapproved_collec': unapproved_collec, 'activities': activities}
        return render(request, 'niqati/approve.html', context)


@login_required
@permission_required('niqati.view_general_report', raise_exception=True)
def general_report(request):
    users = User.objects.annotate(point_sum=Sum('code__category__points')).filter(point_sum__gt=0).order_by('-point_sum')
    return render(request, 'niqati/general_report.html', {'users': users})
