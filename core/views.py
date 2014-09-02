# -*- coding: utf-8  -*-
from datetime import datetime, timedelta, date

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from activities.models import Activity
from activities.utils import get_approved_activities
from books.models import Book
from .models import Announcement

def portal_home(request):
    # If the user is logged in, return the admin dashboard;
    # If not, return the front-end homepage
    if request.user.is_authenticated():
        context = {}
        # --- activities ---
        current_year_activities = Activity.objects.all()
        # count only approved activites
        approved_activities = get_approved_activities()
        context['activity_count'] = approved_activities.count()
        
        today = date.today()
        next_week = today + timedelta(weeks=1)
        upcoming_activities = filter(lambda a: a.get_next_episode() is not None, get_approved_activities())
        next_week_activities = filter(lambda a: a.get_next_episode().start_date <= next_week, upcoming_activities)
        context['upcoming_activities'] = next_week_activities[::-1]
        
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
