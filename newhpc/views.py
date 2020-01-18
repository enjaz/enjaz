# -*- coding: utf-8  -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.decorators import csrf
from django.http import JsonResponse
from django.shortcuts import render
from core import decorators
from .models import FaqCategory, FaqQuestion, BlogPostArabic, BlogPostEnglish, NewsletterMembership, BlogVideo, Speaker
from .forms import *
from events.models import Event, Session, TimeSlot,SessionRegistration
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
import events.utils



# enjazportal.com/riyadh HPC Riyadh :

def riy_ar_index(request):
    context = {}
    return render(request,'newhpc/arabic/riy_ar_index.html',context)

def riy_en_index(request):
    context = {}
    return render(request,'newhpc/english/riy_en_index.html',context)

def riy_coming_soon(request):
    context = {}
    return render(request,'newhpc/arabic/riy_coming_soon.html',context)

# def riy_ar_registration(request):
#     context = {}
#     return render(request,'newhpc/arabic/riy_ar_registeration.html',context)
event = Event.objects.get(code_name = 'hpc2-r')

@login_required
def riy_ar_registration(request):

    timeslots = TimeSlot.objects.filter(event=event ,parent__isnull=True)
    session = Session.objects.get(event=event, code_name='general')
    registration = SessionRegistration.objects.filter(session=session, user=request.user,is_deleted=False).first()
    if registration:
        registred_to_program = True
    else :
        registred_to_program = False

    if timeslots.filter(image__isnull=False):
        have_image = True
    else:
        have_image = False

    context = {'timeslots': timeslots,
               'event': event,
               'have_image': have_image,
               'registred_to_program': registred_to_program}

    if event.registration_opening_date and timezone.now() < event.registration_opening_date and not request.user.is_superuser and not events.utils.is_organizing_team_member(request.user, event) and not events.utils.is_in_entry_team(request.user):
        raise Http404
    elif event.registration_closing_date and timezone.now() > event.registration_closing_date:
        return HttpResponseRedirect(reverse('events:registration_closed',
                                                args=(event.code_name,)))

    return render(request, 'newhpc/arabic/riy_ar_eng_registeration_test.html', context)

@login_required
def register_general_program(request):
    session = Session.objects.get(event=event, code_name='general')
    registration = SessionRegistration.objects.filter(session=session, user=request.user).first()
    if not registration:
        registration = SessionRegistration.objects.create(session=session,
                                                          user=request.user,
                                                          is_approved=True)
    return HttpResponseRedirect(reverse('newhpc:riy_ar_registration',
                                        ))



@login_required
def list_sessions(request, event_code_name, pk):
    event = get_object_or_404(Event, code_name=event_code_name)
    timeslot = TimeSlot.objects.get(event=event, pk=pk)
    children_total = timeslot.session_set.count() + timeslot.children.count()
    if timeslot.limit:
        remaining_number = timeslot.limit - request.user.session_registrations.filter(session__time_slot=timeslot,is_deleted=False).count()
    else:
        remaining_number = 1
    limit = events.utils.get_timeslot_limit(timeslot)
    context = {'timeslot': timeslot,
               'event': event,
               'children_total':children_total,
               'remaining_number':remaining_number,
               'limit':limit}

    if event.registration_opening_date and timezone.now() < event.registration_opening_date and \
        not request.user.is_superuser and \
        not events.utils.is_organizing_team_member(request.user, event) and \
        not events.utils.is_in_entry_team(request.user):
        raise Http404
    elif event.registration_closing_date and timezone.now() > event.registration_closing_date:
        return HttpResponseRedirect(reverse('events:registration_closed',
                                                args=(event.code_name,)))

    return render(request,  'newhpc/sessions_list.html', context)

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
    return HttpResponseRedirect('/static/static/newhpc/media/file.pdf')

def list_speakers(request, lang):
    if lang == 'ar':
        lang2 = 'arabic'
    elif lang == 'en':
        lang2 = 'english'
    # TODO: FIx hard code in defining current year for filter
    speakers = Speaker.objects.filter(version__year="2020")
    context = {'speakers': speakers, 'year': '2020'}
    return render(request, 'newhpc/'+lang2+'/riy_list_speakers.html', context)

# enjazportal.com/jeddah HPC Jeddah :
def jed_en_research(request):
    context = {}
    return render(request,'newhpc/english/jeddah/jed_en_research.html',context)

# enjazportal.com/alahsa HPC Al Ahsa :
def ahs_en_research(request):
    context = {}
    return render(request,'newhpc/english/alahsa/ahs_en_research.html',context)
