# -*- coding: utf-8  -*-
from datetime import datetime, timedelta, date

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from activities.models import Activity
from books.models import Book
from .models import Announcement, Publication


def portal_home(request):
    # If the user is logged in, return the admin dashboard;
    # If not, return the front-end homepage
    if request.user.is_authenticated():
        context = {}
        # --- activities ---

        approved_activities = Activity.objects.approved().current_year().for_user_gender(request.user).for_user_city(request.user)
        # count only approved activites
        context['activity_count'] = Activity.objects.approved().current_year().count()
        
        today = date.today()
        next_week = today + timedelta(weeks=1)
        next_week_activities = approved_activities.filter(episode__start_date__gte=today,
                                                          episode__start_date__lte=next_week).order_by('episode__start_date')
        context['upcoming_activities'] = next_week_activities
        
        # --- niqati -------
        context['niqati_sum'] = sum(code.category.points for code in request.user.code_set.all())
        context['niqati_count'] = request.user.code_set.count()
        context['latest_entries'] = request.user.code_set.all()[::-1][:5]
        
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
