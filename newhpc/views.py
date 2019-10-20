# -*- coding: utf-8  -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from .models import FaqCategory, FaqQuestion
from .forms import *

# Create your views here.
# enjazportal.com/riyadh/ar HPC Riyadh arabic and english homepage:
"""
def riy_ar_index(request):
    context = {}
    return render(request,'newhpc/arabic/riy_ar_index.html',context)

def riy_en_index(request):
    context = {}
    return render(request,'newhpc/english/riy_en_index.html',context)
"""

def riy_en_research(request):
    context = {}
    return render(request,'newhpc/english/riy_en_research.html',context)

def show_about(request, lang):
    if lang == 'ar':
        lang2 = 'arabic'
    elif lang == 'en':
        lang2 = 'english'
    return render(request, 'newhpc/'+lang2+'/riy_'+lang+'_about.html')

@login_required
def add_FaqCategory(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        instance = FaqCategory()
        form = FaqCategoryForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
    elif request.method == 'GET':
        form = FaqCategoryForm()
    context = {'form' : form}
    return render(request, 'newhpc/english/administrative/add_faq_category.html', context)

@login_required
def add_FaqQuestion(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        instance = FaqQuestion()
        form = FaqQuestionForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
    elif request.method == 'GET':
        form = FaqQuestionForm()
    context = {'form' : form}
    return render(request, 'newhpc/english/administrative/add_faq_question.html', context)

def list_FAQs(request, lang):
    if lang == 'ar':
        lang2 = 'arabic'
    elif lang == 'en':
        lang2 = 'english'
    categories = FaqCategory.objects.all()
    faqs = FaqQuestion.objects.all()
    context = {'categories': categories,
               'faqs': faqs}
    return render(request, 'newhpc/'+lang2+'/'+lang+'_list_FAQ.html', context)

@login_required
def add_prev_version(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        instance = PreviousVersion()
        form = PreviousVersionForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
    elif request.method == 'GET':
        form = PreviousVersionForm()
    context = {'form' : form}
    return render(request, 'newhpc/english/administrative/add_prev_version.html', context)

@login_required
def add_prev_statistic(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        instance = PreviousStatistics()
        form = PreviousStatisticsForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
    elif request.method == 'GET':
        form = PreviousStatisticsForm()
    context = {'form' : form}
    return render(request, 'newhpc/english/administrative/add_prev_statistics.html', context)

@login_required
def add_leader(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        instance = HpcLeader()
        form = HpcLeaderForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
    elif request.method == 'GET':
        form = HpcLeaderForm()
    context = {'form' : form}
    return render(request, 'newhpc/english/administrative/add_leader.html', context)

@login_required
def add_media_sponsor(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        instance = MediaSponser()
        form = MediaSponserForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
    elif request.method == 'GET':
        form = MediaSponserForm()
    context = {'form' : form}
    return render(request, 'newhpc/english/administrative/add_media_sponsor.html', context)

@login_required
def add_winner(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        instance = Winner()
        form = WinnerForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
    elif request.method == 'GET':
        form = WinnerForm()
    context = {'form' : form}
    return render(request, 'newhpc/english/administrative/add_winner.html', context)

def admin_prev_versions(request):
    return render(request, 'newhpc/english/administrative/prev_versions.html')

def list_prev_versions(request):
    pass

def show_prev_version(request, version_id):
    pass
