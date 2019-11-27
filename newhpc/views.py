# -*- coding: utf-8  -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.decorators import csrf
from django.http import JsonResponse
from django.shortcuts import render
from core import decorators
from .models import FaqCategory, FaqQuestion, BlogPostArabic, BlogPostEnglish, NewsletterMembership, BlogVideo
from .forms import *

# Create your views here.
# enjazportal.com/riyadh/ar HPC Riyadh arabic and english homepage:

def riy_ar_index(request):
    context = {}
    return render(request,'newhpc/arabic/riy_ar_index.html',context)

def riy_en_index(request):
    context = {}
    return render(request,'newhpc/english/riy_en_index.html',context)

def riy_coming_soon(request):
    context = {}
    return render(request,'newhpc/arabic/riy_coming_soon.html',context)

def riy_ar_registration(request):
    context = {}
    return render(request,'newhpc/arabic/riy_ar_registeration.html',context)
def riy_en_registration(request):
    context = {}
    return render(request,'newhpc/english/riy_en_registeration.html',context)

def riy_ar_exhibition(request):
    context = {}
    return render(request,'newhpc/arabic/riy_ar_exhibition.html',context)
def riy_en_exhibition(request):
    context = {}
    return render(request,'newhpc/english/riy_en_exhibition.html',context)

def riy_en_research(request):
    context = {}
    return render(request,'newhpc/english/riy_en_research.html',context)
# jeddah


def jed_ar_index(request):
    context = {}
    return render(request,'newhpc/arabic/jed_ar_index.html',context)

def jed_en_index(request):
    context = {}
    return render(request,'newhpc/english/jed_en_index.html',context)

def jed_coming_soon(request):
    context = {}
    return render(request,'newhpc/arabic/jed_coming_soon.html',context)

def jed_ar_registration(request):
    context = {}
    return render(request,'newhpc/arabic/jed_ar_registeration.html',context)
def jed_en_registration(request):
    context = {}
    return render(request,'newhpc/english/jed_en_registeration.html',context)

def jed_ar_exhibition(request):
    context = {}
    return render(request,'newhpc/arabic/jed_ar_exhibition.html',context)
def jed_en_exhibition(request):
    context = {}
    return render(request,'newhpc/english/jed_ar_exhibition.html',context)

def jed_en_research(request):
    context = {}
    return render(request,'newhpc/english/jed_en_research.html',context)

# ah

def ahs_en_research(request):
    context = {}
    return render(request,'newhpc/english/ahs_en_research.html',context)

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
    tech_qs = FaqQuestion.objects.filter(is_tech=True)
    non_tech_qs = FaqQuestion.objects.filter(is_tech=False)
    faqs = FaqQuestion.objects.all()
    context = {'categories': categories,
               'tech_qs': tech_qs,
               'non_tech_qs': non_tech_qs}
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
    versions = PreviousVersion.objects.all()
    context = {'versions': versions}
    return render(request, 'newhpc/arabic/ar_prev_versions.html', context)

def show_version(request, version_year):
    version = PreviousVersion.objects.get(year=version_year)
    speakers = version.speaker_set.filter(is_top_speaker=True)
    context = {'version': version,
               'speakers': speakers}
    return render(request, 'newhpc/arabic/ar_show_version.html', context)

def show_speakers(request, version_year):
    version = PreviousVersion.objects.get(year=version_year)
    context = {'version': version,
               'range': range(2)}
    return render(request, 'newhpc/arabic/all_speakers.html', context)

def main_media(request, lang):
    if lang == 'ar':
        lang2 = 'arabic'
        posts = BlogPostArabic.objects.all()
    elif lang == 'en':
        lang2 = 'english'
        posts = BlogPostEnglish.objects.all()
    videos = BlogVideo.objects.all()
    context = {'posts': posts, 'videos': videos}
    return render(request, 'newhpc/'+lang2+'/main_media.html', context)

def show_post(request, lang, post_id):
    if lang == 'ar':
        lang2 = 'arabic'
        post = get_object_or_404(BlogPostArabic, pk=post_id)
    elif lang == 'en':
        lang2 = 'english'
        post = get_object_or_404(BlogPostEnglish, pk=post_id)
    context = {'post': post}
    return render(request, 'newhpc/'+lang2+'/show_post.html', context)

@decorators.post_only
@decorators.ajax_only
@csrf.csrf_exempt
def handle_newsletter_signup(request):
    form = NewsletterMembershipForm(request.POST)
    response_data = {}
    if form.is_valid():
        email = form.cleaned_data['email']
        previous_membership = NewsletterMembership.objects.filter(email=email).exists()
        if previous_membership:
            response_data['message'] = 'previous'
            raise Exception("previous")
        else:
            response_data['message'] = 'success'
            form.save()
    else:
        response_data['message'] = 'invalid'
        raise Exception("invalid")
    return JsonResponse(response_data)

@login_required
def list_newsletter_members(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    members = NewsletterMembership.objects.all()
    context = {'members': members}
    return render(request, 'newhpc/english/administrative/list_news_members.html', context)

def show_media_file(request, lang):
    return render(request,'newhpc/arabic/riy_coming_soon.html')