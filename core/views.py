# -*- coding: utf-8  -*-
from datetime import datetime, timedelta, date

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from clubs.models import Club, College, city_choices
from activities.models import Activity, Episode
from books.models import Book
from .models import Announcement, Publication, StudentClubYear
from niqati.models import Code_Order, Code
from media.models import FollowUpReport, Story
from accounts.utils import get_user_gender


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
        context['latest_entries'] = request.user.code_set.current_year().order_by('-redeem_date')[::-1][:5]

        # --- books --------
        context['books_count'] = Book.objects.count()
        context['my_books_count'] = request.user.book_contributions.count()
        context['latest_books'] = Book.objects.all()[::-1][:5] # TODO: update to be gender-segregated
        
        # --- announcements 
        context['student_researches'] = Announcement.objects.filter(type='R')[::-1] # show last first
        context['external_announcements'] = Announcement.objects.filter(type='E')[::-1]
        context['major_program_announcement'] = None
        if Announcement.objects.filter(type='M').count() > 0:
            context['major_program_announcement'] = Announcement.objects.filter(type='M')[0]
        
        return render(request, 'home.html', context) # the dashboard
    else:
        return render(request, 'front/home_front.html')


def visit_announcement(request, pk):
    announce = get_object_or_404(Announcement, pk=pk)
    announce.visits += 1
    announce.save()
    return HttpResponseRedirect(announce.url)


def about_sc(request, template_name="about_sc.html"):
    return render(request, template_name, {"publications": Publication.objects.all()}) # the dashboard

@login_required
def indicators(request, city=""):
    if not request.user.is_superuser:
        raise PermissionDenied

    if city:
        current_year = StudentClubYear.objects.get_current()
        city_codes = [city_pair[0] for city_pair in city_choices]
        if not city in city_codes:
            raise Http404
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
            month_orders = Code_Order.objects.distinct().filter(episode__activity__is_approved=True,
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

            club.month_generated_codes = Code.objects.distinct().filter(collection__parent_order__episode__activity__is_approved=True,
                                                                        collection__parent_order__episode__activity__primary_club=club,
                                                                        collection__parent_order__episode__start_date__gte=last_month,
                                                                        collection__parent_order__episode__start_date__lt=timezone.now().date())\
                                                                .count()
            club.month_entered_codes = Code.objects.distinct().filter(collection__parent_order__episode__activity__is_approved=True,
                                                                      collection__parent_order__episode__activity__primary_club=club,
                                                                      collection__parent_order__episode__start_date__gte=last_month,
                                                                      collection__parent_order__episode__start_date__lt=timezone.now().date(),
                                                                      user__isnull=False).count()
            club.used_direct_entry = Code_Order.objects.distinct().filter(episode__activity__is_approved=True,
                                                                          episode__activity__primary_club=club,
                                                                          episode__start_date__gte=last_month,
                                                                          episode__start_date__lt=timezone.now().date(),
                                                                          code_collection__students__isnull=False).exists()
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
            gender = get_user_gender(user)
            if gender == 'M':
                male_count += 1
            elif gender == 'F':
                female_count += 1


        # Order review interval
        month_orders = Code_Order.objects.distinct().filter(is_approved=True,
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
                   city_choices}

    return render(request, 'indicators.html', context)
