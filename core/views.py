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
from activities.models import Activity
from books.models import Book
from .models import Announcement, Publication, StudentClubYear
from niqati.models import Code_Order, Code
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
        next_week_activities = filtered_activities.filter(episode__start_date__gte=today,
                                                          episode__start_date__lte=next_week).order_by('episode__start_date')
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
        last_month = timezone.now() - timedelta(30)

        clubs_by_niqati = Club.objects.current_year()\
                                              .visible()\
                                              .filter(city=city)
        # It gets funky if we try to do it through Django's ORM
        for club in clubs_by_niqati:
            club.month_activities = club.primary_activity.approved().filter(episode__start_date__gte=last_month).count()
            club.month_code_orders = Code_Order.objects.filter(episode__activity__is_approved=True,
                                                               episode__activity__primary_club=club,
                                                               episode__start_date__gte=last_month).count()
            club.month_generated_codes = Code.objects.distinct().filter(collection__parent_order__episode__activity__is_approved=True,
                                                                        collection__parent_order__episode__activity__primary_club=club,
                                                                        collection__parent_order__episode__start_date__gte=last_month).count()
            club.month_entered_codes = Code.objects.distinct().filter(collection__parent_order__episode__activity__is_approved=True,
                                                                      collection__parent_order__episode__activity__primary_club=club,
                                                                      collection__parent_order__episode__start_date__gte=last_month,
                                                                      user__isnull=False).count()
        clubs_by_members = Club.objects.current_year()\
                                       .visible()\
                                       .filter(city=city)\
                                       .annotate(member_count=Count('members'))\
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
                
        context = {'male_count': male_count,
                   'female_count': female_count,
                   'users_by_niqati_points': users_by_niqati_points,
                   'clubs_by_niqati': clubs_by_niqati,
                   'city_colleges': city_colleges,
                   'clubs_by_members': clubs_by_members,
                   }
    else:
        context = {'city_choices':
                   city_choices}

    return render(request, 'indicators.html', context)
