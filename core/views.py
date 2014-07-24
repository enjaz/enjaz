# -*- coding: utf-8  -*-
from datetime import datetime, timedelta, date

from django.shortcuts import render

from activities.models import Activity
from books.models import Book

def portal_home(request):
    # If the user is logged in, return the admin dashboard;
    # If not, return the front-end homepage
    if request.user.is_authenticated():
        context = {}
        # --- activities ---
        current_year_activities = Activity.objects.all()
        # count only approved activites
        approved_activities = []
        for a in current_year_activities:
            if a.is_approved(): approved_activities.append(a)
        context['activity_count'] = len(approved_activities)
        
        today = date.today()
        next_week = today + timedelta(weeks=1)
        next_week_activities = filter(lambda a: a.get_first_date() >= today and a.get_first_date() <= next_week, Activity.objects.all()) # filter(date__gte=today , date__lte=next_week)
        # show only approved activities
        upcoming_activities = []
        for a in next_week_activities:
            if a.is_approved(): upcoming_activities.append(a)
        context['upcoming_activities'] = upcoming_activities[::-1]
        
        # --- niqati -------
        context['niqati_sum'] = sum(code.category.points for code in request.user.code_set.all())
        context['niqati_count'] = request.user.code_set.count()
        context['latest_entries'] = request.user.code_set.all()[::-1][:5]
        
        # --- books --------
        context['books_count'] = Book.objects.count()
        context['my_books_count'] = request.user.book_contributions.count()
        context['latest_books'] = Book.objects.all()[::-1][:5]
        
        return render(request, 'home.html', context) # the dashboard
    else:
        return render(request, 'front/home_front.html')
