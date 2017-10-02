# -*- coding: utf-8  -*-
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils import timezone
from dal import autocomplete
import re

from . import decorators, utils
from .models import Publication, StudentClubYear
from .forms import DebateForm
from activities.models import Activity, Episode
from bulb.models import Book
from clubs.models import Club, College, city_code_choices
from constance import config
from niqati.models import Order, Code
from media.models import FollowUpReport, Story
import accounts.utils
import clubs.utils


def portal_home(request):
    # If the user is logged in, return the admin dashboard;
    # If not, return the front-end homepage
    if request.user.is_authenticated():
        context = {}
        # --- activities ---

        approved_activities = Activity.objects.approved().current_year()
        filtered_activities = (approved_activities.for_user_gender(request.user).for_user_city(request.user) | \
                               approved_activities.for_user_clubs(request.user)).distinct()
        # count only approved activites
        context['activity_count'] = Activity.objects.approved().current_year().count()

        today = date.today()
        next_week = today + timedelta(weeks=1)
        next_week_activities = filtered_activities.upcoming().filter(episode__start_date__gte=today,
                                                                     episode__start_date__lte=next_week)\
                                                             .order_by('episode__start_date')
        context['upcoming_activities'] = next_week_activities

        # --- niqati -------
        niqati_sum = request.user.code_set.current_year().aggregate(niqati_sum=Sum('points'))['niqati_sum']
        context['niqati_sum'] = niqati_sum
        context['niqati_count'] = request.user.code_set.current_year().count()
        context['latest_entries'] = request.user.code_set.current_year().order_by('-redeem_date')[:5]

        # --- books --------
        context['book_sample'] = Book.objects.current_year().for_user_city(request.user).available().order_by("?")[:6]
        context['book_count'] = Book.objects.current_year().undeleted().count()
        context['my_book_count'] = request.user.book_giveaways.current_year().undeleted().count()

        return render(request, 'home.html', context) # the dashboard
    else:
        return render(request, 'front/home_front.html')


def about_sc(request, template_name="about_sc.html"):
    return render(request, template_name, {"publications": Publication.objects.all()}) # the dashboard

@login_required
def indicators(request, city_code=""):
    if not request.user.is_superuser and \
       not clubs.utils.is_presidency_coordinator_or_deputy(request.user):
        raise PermissionDenied

    if city_code:
        city = accounts.utils.get_city_from_code(city_code)
        # To avoid user fuck-ups entering non-standard city-code.
        if not city:
            raise Http404
        current_year = StudentClubYear.objects.get_current()
        last_month = timezone.now().date() - timedelta(30)
        city_clubs = Club.objects.current_year()\
                                 .visible()\
                                 .filter(city=city)
        clubs_by_media = city_clubs
        for club in clubs_by_media:
            club.episode_count = Episode.objects.filter(activity__primary_club=club,
                                                        activity__is_approved=True,
                                                        activity__is_deleted=False,
                                                        start_date__gte=last_month,
                                                        start_date__lt=timezone.now().date()).count()
            month_reports = FollowUpReport.objects.filter(episode__activity__primary_club=club,
                                                          episode__end_date__gte=last_month,
                                                          episode__end_date__lt=timezone.now().date())
            club.report_count = month_reports.count()
            total_report_interval = 0
            for report in month_reports:
                total_report_interval += (report.date_submitted.date() - report.episode.end_date).days
            if club.report_count:
                club.report_interval = total_report_interval / club.report_count
            else:
                club.report_interval = '-'
            month_stories = Story.objects.filter(episode__activity__primary_club=club,
                                                 episode__end_date__gte=last_month,
                                                 episode__end_date__lt=timezone.now().date())
            club.story_count = month_stories.count()
            total_story_interval = 0
            for story in month_stories:
                total_story_interval += (story.date_submitted.date() - story.episode.end_date).days
            if club.story_count:
                club.story_interval = total_story_interval / club.story_count
            else:
                club.story_interval = '-'

        clubs_by_niqati = city_clubs
        for club in clubs_by_niqati:
            club.month_episodes = Episode.objects.filter(activity__primary_club=club,
                                                         activity__is_approved=True,
                                                         activity__is_deleted=False,
                                                         start_date__gte=last_month,
                                                         start_date__lt=timezone.now().date()).count()
            month_orders = Order.objects.distinct().filter(episode__activity__is_approved=True,
                                                                episode__activity__primary_club=club,
                                                                episode__start_date__gte=last_month,
                                                                episode__start_date__lt=timezone.now().date())
            total_order_interval = 0
            for order in month_orders:
                total_order_interval += (order.episode.start_date - order.date_ordered.date()).days

            club.month_code_orders = month_orders.count()

            if club.month_code_orders: # Not zero
                club.niqati_order_interval = total_order_interval / club.month_code_orders
            else:
                club.niqati_order_interval = '-'

            episode_content_type = ContentType.objects.get(model="episode")
            month_episode_pks = Episode.objects.filter(activity__is_approved=True,
                                                       activity__primary_club=club,
                                                       start_date__gte=last_month,
                                                       start_date__lt=timezone.now().date()).values_list("pk", flat=True)
            club.month_generated_codes = Code.objects.distinct().filter(content_type=episode_content_type,
                                                                        object_id__in=month_episode_pks)\
                                                                .count()
            club.month_entered_codes = Code.objects.distinct().filter(content_type=episode_content_type,
                                                                      object_id__in=month_episode_pks,
                                                                      user__isnull=False).count()
            club.used_direct_entry = Order.objects.distinct().filter(episode__activity__is_approved=True,
                                                                     episode__activity__primary_club=club,
                                                                     episode__start_date__gte=last_month,
                                                                     episode__start_date__lt=timezone.now().date(),
                                                                     collection__students__isnull=False).exists()
        clubs_by_members = city_clubs.annotate(member_count=Count('members'))\
                                     .order_by('-member_count')
        users_by_niqati_points = User.objects.filter(common_profile__city=city,
                                                     code__year=current_year)\
                                             .annotate(point_sum=Sum('code__points'))\
                                             .filter(point_sum__gt=0)\
                                             .order_by('-point_sum')[:20]
        city_colleges = College.objects.filter(city=city)
        # It gets funky if we try to do it through Django's ORM
        for college in city_colleges:
            college.active_count = college.commonprofile_set.filter(user__is_active=True).count()
            if college.commonprofile_set.exists():
                college.active_percentage = "%.2f%%" % (float(college.commonprofile_set.filter(user__is_active=True).count()) / college.commonprofile_set.count() * 100)
            else:
                college.active_percentage = '-'
        male_count = 0
        female_count = 0
        for user in users_by_niqati_points:
            gender = accounts.utils.get_user_gender(user)
            if gender == 'M':
                male_count += 1
            elif gender == 'F':
                female_count += 1


        # Order review interval
        month_orders = Order.objects.distinct().filter(is_approved=True,
                                                            episode__start_date__gte=last_month,
                                                            episode__start_date__lt=timezone.now().date(),
                                                            episode__activity__primary_club__city=city)
        male_orders = month_orders.filter(episode__activity__primary_club__gender='M')
        female_orders = month_orders.filter(episode__activity__primary_club__gender='F')
        male_total_intervals = 0
        female_total_intervals = 0
        for order in male_orders:
            # To skip orders without reviews (i.e. created through the admin interface)
            try:
                date_reviewed = order.review_set.first().date_reviewed.date()
            except AttributeError:
                continue
            male_total_intervals += (date_reviewed - order.date_ordered.date()).days
        for order in female_orders:
            # To skip orders without reviews (i.e. created through the admin interface)
            try:
                date_reviewed = order.review_set.first().date_reviewed.date()
            except AttributeError:
                continue

            female_total_intervals += (date_reviewed - order.date_ordered.date()).days

        if male_orders.exists():
            male_niqati_approval_interval = male_total_intervals / male_orders.count()
        else:
            male_niqati_approval_interval = '-'
        if female_orders.exists():
            female_niqati_approval_interval = female_total_intervals / female_orders.count()
        else:
            female_niqati_approval_interval = '-'

        context = {'male_count': male_count,
                   'female_count': female_count,
                   'users_by_niqati_points': users_by_niqati_points,
                   'clubs_by_niqati': clubs_by_niqati,
                   'clubs_by_media': clubs_by_media,
                   'city_colleges': city_colleges,
                   'clubs_by_members': clubs_by_members,
                   'male_niqati_approval_interval': male_niqati_approval_interval,
                   'female_niqati_approval_interval': female_niqati_approval_interval,
                   }
    else:
        context = {'city_choices':
                   city_code_choices}

    return render(request, 'indicators.html', context)

@decorators.ajax_only
@login_required
def cancel_twitter_connection(request):
    try:
        common_profile = request.user.common_profile
    except ObjectDoesNotExist:
        return {}

    common_profile.canceled_twitter_connection = True
    common_profile.save()
    return {}

@decorators.ajax_only
def update_user_count(request):
    start_date = timezone.make_aware(datetime(2016, 9, 18, 7), timezone.get_default_timezone())
    user_count = User.objects.filter(date_joined__gte=start_date).count()
    return {'user_count': user_count}

def debate(request):
    url = config.DEBATE_URL
    context ={'url': url}
    if request.user.is_superuser or \
       request.user.username in ['alsaaid031', 'alkaabba039', 'aljuhani518']:
        if request.method == 'POST':
            form = DebateForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("debate"))
        elif request.method == 'GET':
            form = DebateForm(initial={'url': url})
        context['form'] = form
    return render(request, 'debate.html', context)

class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return User.objects.none()

        qs = User.objects.filter(is_active=True)

        if self.q:
            search_fields = [re.sub('^user__', '', field) for field in utils.BASIC_SEARCH_FIELDS]
            print search_fields
            qs = utils.get_search_queryset(qs, search_fields, self.q)

        return qs

    def get_result_label(self, item):
        full_name = accounts.utils.get_user_ar_full_name(item) or item.username
        return"%s <bdi style='font-family: monospace;'>(%s)</bdi>" % (full_name, item.username)
