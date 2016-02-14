# -*- coding: utf-8  -*-
import requests
import datetime

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.http import urlquote
from django.db.models import Sum
from django.core.exceptions import PermissionDenied
from django.views.decorators import csrf

from post_office import mail
from accounts.models import get_gender
from core import decorators
from core.models import StudentClubYear
from activities.models import Activity, Evaluation
from activities.forms import EvaluationForm
from activities.utils import get_club_notification_to, get_club_notification_cc
from clubs.models import Club, city_choices
from clubs.utils import has_coordination_to_activity, get_user_coordination_and_deputyships, can_review_any_niqati, is_coordinator_of_any_club
from niqati.models import Category, Code, Code_Order, Code_Collection, Review, COUPON, SHORT_LINK
from niqati.forms import OrderForm, RedeemCodeForm


current_year = StudentClubYear.objects.get_current()

@login_required
def index(request):
    if request.user.has_perms('niqati.view_general_report'): # Superuser
        return HttpResponseRedirect(reverse('niqati:general_report'))
    elif can_review_any_niqati(request.user):
        return HttpResponseRedirect(reverse('niqati:list_pending_orders'))
    elif is_coordinator_of_any_club(request.user):
        user_clubs = get_user_coordination_and_deputyships(request.user)
        user_club = user_clubs.first()
        context = {'user_club': user_club}
        return render(request, "niqati/intro_coordinators.html", context)
    else: # Student Views
        return HttpResponseRedirect(reverse('niqati:submit'))

@login_required
@decorators.get_only
def redeem(request, code=""):
    """
    GET: show the code submission form.
    POST: submit a code.
    """    
    if current_year.niqati_closure_date and timezone.now() > current_year.niqati_closure_date:
        return render(request, "niqati/submit_closed.html")
    elif is_coordinator_of_any_club(request.user):
        user_club = request.user.coordination.current_year().first()
        context = {'user_club': user_club}
        return render(request, "niqati/submit_coordinators.html", context)
    else:
        # Code string can be passed in the URL, or as a GET parameter.
        if not code:
            code = request.GET.get('code')
        form = RedeemCodeForm(request.user, initial={'string': code})
        eval_form = EvaluationForm()
        return render(request, "niqati/submit.html", {"form": form,  "eval_form": eval_form})

@login_required
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def claim_code(request):
    form = RedeemCodeForm(request.user, request.POST)
    eval_form = EvaluationForm(request.POST)
    if form.is_valid() and eval_form.is_valid():
        result = form.process()
        eval_form.save(form.code.collection.parent_order.episode, request.user)
        return result
    else:
        errors = form.errors
        errors.update(eval_form.errors)
        return {'errors': errors}

@login_required
def student_report(request, username=None):
    # Only the superuser can see a specific user.  Coordinators will
    # get an introduction page to Niqati becaues they are not supposed
    # to register any codes.
    if username and not request.user.has_perm('niqati.view_code'):
        raise PermissionDenied
    elif request.user.coordination.current_year().exists():
        user_club = request.user.coordination.current_year().first()
        context = {'user_club': user_club}
        return render(request, "niqati/submit_coordinators.html", context)

    if username:
        niqati_user = get_object_or_404(User, username=username)
    else:
        niqati_user = request.user
    # TODO: sort codes
    total_points = niqati_user.code_set.current_year().aggregate(total_points=Sum('points'))['total_points']
    if total_points is None:
        total_points = 0
    context = {'total_points': total_points, 'niqati_user': niqati_user}
    return render(request, 'niqati/student_report.html', context)

# Club Views
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

    # If it has been two weeks since the end of the activity, don't
    # alow niqati requests.
    last_episode = activity.episode_set.order_by('-end_date', '-end_time').first()
    if timezone.now().date() > last_episode.end_date + datetime.timedelta(14):
        return render(request, 'niqati/activity_orders.html',
                      {'activity': activity, 'active_tab': 'niqati',
                       'error': 'closed'})
    if request.method == 'POST':
        form = OrderForm(request.POST, activity=activity, user=request.user)
        if form.is_valid():
            order = form.save()
            if order:
                reviewing_parent = activity.primary_club.get_next_niqati_reviewing_parent()
                # Make sure that a coordinator was assigned to the
                # reviewing club before trying to send an email
                # notification.
                if reviewing_parent and reviewing_parent.coordinator:
                    list_pending_orders_url = reverse('niqati:list_pending_orders')
                    full_url = request.build_absolute_uri(list_pending_orders_url)
                    email_context = {'order': order, 'full_url': full_url}
                    mail.send([reviewing_parent.coordinator.email],
                              template="niqati_order_submitted",
                              context=email_context)

                    msg = u"تم إرسال الطلب؛ و سيتم إنشاء النقاط فور الموافقة عليه"
                    messages.add_message(request, messages.SUCCESS, msg)
                elif not reviewing_parent:
                    order.is_approved = True
                    order.save()
                    order.create_codes()
            else:
                msg = u"لم ينشأ أي طلب لأنك لم تدخل أي رقم."
                messages.add_message(request, messages.WARNING, msg)
            return HttpResponseRedirect(reverse("activities:niqati_orders", args=(activity.id, )))
        else:
            msg = u"الرجاء ملء النموذج بشكل صحيح."
            messages.add_message(request, messages.ERROR, msg)
    elif request.method == 'GET':
        form = OrderForm(activity=activity, user=request.user)
    return render(request, 'niqati/activity_orders.html', {'activity': activity,
                                                           'form': form,
                                                           'active_tab': 'niqati'})

@login_required
def download_collection(request, pk, download_type):
    collection = get_object_or_404(Code_Collection, pk=pk)
    activity = collection.parent_order.episode.activity
    domain = Site.objects.get_current().domain
    domain =  'enjazportal.com' # REMOVE

    if not has_coordination_to_activity(request.user, activity) and \
       not request.user.is_superuser:
        raise PermissionDenied

    if download_type == COUPON:
        endpoint = "http://api.qrserver.com/v1/create-qr-code/?size=180x180&data=" + domain

        response = render(request, 'niqati/includes/coupons.html', {"collection": collection,
                                                                   "domain": domain,
                                                                   "endpoint": endpoint})
    elif download_type == SHORT_LINK:
        response = render(request, 'niqati/includes/links.html', {"collection": collection})
    # Mark codes as downloaded
    collection.date_downloaded = timezone.now()

    return response

# Management Views

@login_required
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def review_order(request):
    order_pk = request.POST.get('pk')
    action = request.POST.get('action')
    order = get_object_or_404(Code_Order, pk=order_pk)
    niqati_reviewers = Club.objects.niqati_reviewing_parents(order)
    user_clubs = niqati_reviewers.filter(coordinator=request.user) | \
                 niqati_reviewers.filter(deputies=request.user)

    # Permission check
    if request.user.has_perm('niqati.change_code_order'):
        reviewer_club = None
    elif user_clubs.exists():
        reviewer_club = user_clubs.first()
    else: # If not a superuser, nor has reviewer 
        raise PermissionDenied

    email_context = {'order': order}
    
    if action == 'accept':
        is_approved = True

        # If the reviewer belongs to a reviewer club (i.e. not the
        # superuser), then check if we have a niqati reviewing parent.
        # If so, assign the order to them.  If not, consider the order
        # approved and email the submitter.  Otherwise, if the review
        # does not belong to a reviewer club (i.e. superuser),
        # consider the order approved.
        if reviewer_club:
            next_parent = reviewer_club.get_next_niqati_reviewing_parent()
            if next_parent:
                order.assignee = next_parent
                order.is_approved = None
                if next_parent.coordinator:
                    list_pending_orders_url = reverse('niqati:list_pending_orders')
                    full_url = request.build_absolute_uri(list_pending_orders_url)
                    email_context['full_url'] = full_url
                    email_context['last_reviewer'] = reviewer_club
                    email_context['upcoming_reviewer'] = next_parent
                    mail.send(next_parent.coordinator.email,
                              template="niqati_approved_to_next_reviwer",
                              context=email_context)
            else:
                order.assignee = None
                order.is_approved = True
        else: # superuser
            order.assignee = None
            order.is_approved = True

        if order.is_approved:
            order.create_codes()
            niqati_orders_url = reverse('activities:niqati_orders', args=(order.episode.activity.pk,))
            full_url = request.build_absolute_uri(niqati_orders_url)
            email_context['full_url'] = full_url            
            mail.send(get_club_notification_to(order.episode.activity),
                      cc=get_club_notification_cc(order.episode.activity),
                      template="niqati_approved_to_submitter",
                      context=email_context)

    elif action == 'reject':
        is_approved = False
        order.assignee = None
        order.is_approved = False
        niqati_orders_url = reverse('activities:niqati_orders', args=(order.episode.activity.pk,))
        full_url = request.build_absolute_uri(niqati_orders_url)
        email_context['full_url'] = full_url

        mail.send(get_club_notification_to(order.episode.activity),
                  cc=get_club_notification_cc(order.episode.activity),
                  template="niqati_rejected_to_submitter",
                  context=email_context)
    else:
        raise Exception(u'تصرف خاطئ.')

    Review.objects.create(order=order,
                          reviewer=request.user,
                          reviewer_club=reviewer_club,
                          is_approved=is_approved)
    order.save()

@login_required
def list_pending_orders(request):
    user_clubs = get_user_coordination_and_deputyships(request.user)
    user_niqati_reviewing_clubs = user_clubs.filter(can_review_niqati=True)
    if not request.user.has_perm('niqati.change_code') and \
       not user_niqati_reviewing_clubs.exists():
        raise PermissionDenied

    # For the superuser, show all pending requests.
    if request.user.has_perm('niqati.change_code_order'):
        activities_with_pending_orders = Activity.objects.current_year().filter(episode__code_order__isnull=False,
                                                                              episode__code_order__is_approved__isnull=True).distinct()
    else:
        activities_with_pending_orders = Activity.objects.current_year().filter(episode__code_order__assignee__in=user_niqati_reviewing_clubs,
                                                                 episode__code_order__is_approved__isnull=True).distinct()
    context = {'activities_with_pending_orders': activities_with_pending_orders}
    return render(request, 'niqati/approve.html', context)

@login_required
@permission_required('niqati.view_general_report', raise_exception=True)
def general_report(request, city=""):
    if city:
        city_codes = [city_pair[0] for city_pair in city_choices]
        if not city in city_codes:
            raise Http404
        users = User.objects.filter(common_profile__city=city,
                                    code__year=current_year).annotate(point_sum=Sum('code__points')).filter(point_sum__gt=0).order_by('-point_sum')
        context = {'users': users}
    else:
        context = {'city_choices':
                   city_choices}
    return render(request, 'niqati/general_report.html', context)

@login_required
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def get_short_url(request):
    pk = request.POST.get('pk')
    code = get_object_or_404(Code, pk=pk)
    order = code.collection.parent_order
    activity = order.episode.activity
    niqati_reviewers = Club.objects.niqati_reviewing_parents(order)
    user_clubs_niqati_reviewers = niqati_reviewers.filter(coordinator=request.user) | \
                                  niqati_reviewers.filter(deputies=request.user)

    # Only the coordinators and deputies of activities, niqati
    # reviewers and the superuser are allowed to access this API.
    if not has_coordination_to_activity(request.user, activity) and \
       not user_clubs_niqati_reviewers.exists() and \
       not request.user.is_superuser:
        raise PermissionDenied

    if not code.short_link:
        endpoint = "https://api-ssl.bitly.com/v3/shorten?format=txt&access_token=%(api_key)s&longUrl=" % {"api_key": settings.BITLY_KEY}
        domain = Site.objects.get_current().domain
        domain =  'enjazportal.com' # REMOVE
        full_url = urlquote("http://%s%s?code=%s" % (domain, reverse("niqati:submit"), code.code_string))
        response = requests.get(endpoint + full_url)
        short_link = response.text
        short_link = short_link.strip() # remove tailing new lines
        if short_link == "RATE_LIMIT_EXCEEDED":
            raise Exception("تعّر إنشاء أحد الروابط. حدّث الصفحة.")
        short_link = short_link.replace("http:", "https:") # Duh!
        code.short_link = short_link
        code.save()

    return {'url': code.short_link }

