# -*- coding: utf-8  -*-
import random

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.decorators import csrf

from core import decorators
from clubs.models import Club
from activities.models import Activity, Episode
from media.models import FollowUpReport, Story, Article, StoryReview, ArticleReview, StoryTask
from media.forms import FollowUpReportForm, StoryForm, StoryReviewForm, ArticleForm, ArticleReviewForm

# --- Helper functions

def get_media_center():
    return Club.objects.get(english_name="Media Center")

def get_user_clubs(user):
    return user.coordination.all() | user.memberships.all()

# --- Views ---

@login_required
def index(request):
    """
    Redirect to list view.
    """
    return HttpResponseRedirect(reverse('media:list_activities'))
    # TODO: if the user doesn't have proper permissions, just show
    # a welcome page with a link to article submission

@login_required
def list_activities(request):
    """
    Show a list of activities, with recently approved ones marked, together with
    the available options of FollowUpReports and Stories.
    """
    # Get all approved activities
    activities = filter(lambda x: x.is_approved() == True, Activity.objects.all())
    media_center = get_media_center()
    return render(request, 'media/list_activities.html', {'activities': activities,
                                                          'media_center': media_center})

# --- Follow-up Reports ---

@login_required
def list_reports(request):
    """
    Show a list of all reports in a single table.
    """
    # Get all reports
    reports = FollowUpReport.objects.all()
    return render(request, 'media/list_reports.html', {'reports': reports})

#@permission_required('add_followupreport')
@login_required
def submit_report(request, episode_pk):
    """
    Submit a FollowUpReport.
    """
    episode = get_object_or_404(Episode, pk=episode_pk)
    
    # Permission checks
    # (1) The passed episode should be owned by the user's club
    user_clubs = get_user_clubs(request.user)
    if episode.activity.primary_club not in user_clubs and not request.user.is_superuser:
        raise PermissionDenied
    # (2) The passed episode shouldn't already have a report.
    #     Overriding a previous submission shouldn't be allowed
    try:
        report = episode.followupreport
        raise PermissionDenied
    except ObjectDoesNotExist:
        pass
    
    if request.method == 'POST':
        form = FollowUpReportForm(request.POST,
                                  instance=FollowUpReport(pk=episode.pk, # make pk equal to episode pk
                                                                         # to keep things synchronized
                                                          episode=episode,
                                                          submitter=request.user)
                                  )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('activities:show',
                                                args=(episode.activity.pk, )
                                                ))
    else:
        # Initialize the form with initial data from the episode
        form = FollowUpReportForm(initial={# no initial data for the description, because
                                           # the report should contain a description of what
                                           # actually happened, whereas the description
                                           # of the activity isn't necessarily that.
                                           'start_date' : episode.start_date,
                                           'end_date'   : episode.end_date,
                                           'start_time' : episode.start_time,
                                           'end_time'   : episode.end_time,
                                           'location'   : episode.location,
                                           'organizer_count': episode.activity.organizers,
                                           'participant_count': episode.activity.participants,
                                           })
    return render(request, 'media/report_write.html', {'form': form,
                                                       'episode': episode})

@login_required
def show_report(request, episode_pk):
    """
    Show a FollowUpReport.
    """
    episode = get_object_or_404(Episode, pk=episode_pk)
    report = get_object_or_404(FollowUpReport, episode=episode)
    return render(request, 'media/report_read.html', {'report': report})

# --- Stories ---

@login_required
def create_story(request, episode_pk):
    """
    Create a story for an episode.
    """
    episode = get_object_or_404(Episode, pk=episode_pk)
    
    # --- Permission Checks ---
    # (1) The user should be part of the Media Center (either head or member)
    media_center = get_media_center()
    user_clubs = get_user_clubs(request.user)
    if media_center not in user_clubs and not request.user.is_superuser:
        raise PermissionDenied
    # (2) The passed episode shouldn't already have a story.
    #     If so, redirect to the edit view
    try:
        story = episode.story
        return HttpResponseRedirect(reverse('media:edit_story',
                                            args=(episode.pk, )))
    except ObjectDoesNotExist:
        pass
    # (3) The episode should have no task associated with it;
    #     or it should have a task assigned to the user
    #    #TODO
    
    
    if request.method == 'POST':
        form = StoryForm(request.POST,
                         instance=Story(pk=episode.pk, # make pk equal to episode pk
                                                       # to keep things synchronized
                                        episode=episode,
                                        writer=request.user) # This is the only place
                                                             # we specify the writer.
                                                             # The story will be attributed
                                                             # to the author, no matter
                                                             # who edits it later on.
                         )
        if form.is_valid():
            form.save()
            # TODO: resolve task
            return HttpResponseRedirect(reverse('media:show_story',
                                                args=(episode.pk, )))
    else:
        form = StoryForm()
    
    context = {}
    context['form'] = form
    context['episode'] = episode
    # Get the episode's report to include in the context
    try:
        context['report'] = episode.followupreport
    except ObjectDoesNotExist:
        pass
    return render(request, 'media/story_write.html', context)

@login_required
def show_story(request, episode_pk):
    """
    Show a Story.
    """
    # --- Permission Checks ---
    # The user should be part of the Media Center (either head or member)
    if get_media_center() not in get_user_clubs(request.user) and not request.user.is_superuser:
        raise PermissionDenied 
    
    episode = get_object_or_404(Episode, pk=episode_pk)
    story = get_object_or_404(Story, episode=episode)
    try:
        review = story.storyreview
    except ObjectDoesNotExist:
        review = None
    return render(request, 'media/story_read.html', {'story': story,
                                                     'review': review,
                                                     'episode': episode})

@login_required
def edit_story(request, episode_pk):
    """
    Review a Story by writing notes or editing it directly.
    """
    episode = get_object_or_404(Episode, pk=episode_pk)
    story = get_object_or_404(Story, episode=episode)
    try:
        review = StoryReview.objects.get(story=story)
    except ObjectDoesNotExist:
        review = StoryReview(story=story,
                             reviewer=request.user)
    
    # --- Permission Checks ---
    # The user should be part of the Media Center (either head or member)
    media_center = get_media_center()
    user_clubs = get_user_clubs(request.user)
    if media_center not in user_clubs and not request.user.is_superuser:
        raise PermissionDenied    
    
    if request.method == 'POST':
        form = StoryForm(request.POST,
                         instance=Story.objects.get(pk=episode.pk)
                         )
        review_form = StoryReviewForm(request.POST,
                                      instance=review)
        if form.is_valid() and review_form.is_valid():
            form.save()
            review_form.save()
            # TODO: resolve task
            return HttpResponseRedirect(reverse('media:show_story',
                                                args=(episode.pk, )))
    else:
        form = StoryForm(instance=story)
        review_form = StoryReviewForm(instance=review)
    
    context = {}
    context['form'] = form
    if request.user == media_center.coordinator or request.user.is_superuser:
        context['review_form'] = review_form
    else:
        context['review'] = review
    context['episode'] = episode
    # Get the episode's report to include in the context
    try:
        context['report'] = episode.followupreport
    except ObjectDoesNotExist:
        pass
    return render(request, 'media/story_write.html', context)

@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def assign_story_task(request):
    """
    Assign a task to write or edit a story.
    """
    # --- Permission Checks ---
    # The user should be the head of the Media Center
    media_center = get_media_center()
    if request.user != media_center.coordinator and not request.user.is_superuser:
        raise PermissionDenied   
    
    episode = Episode.objects.get(pk=request.POST['episode_pk'])
    if request.POST['assignee'] == 'random':
        assignee = random.choice(media_center.members.all())
    else:
        assignee = User.objects.get(pk=int(request.POST['assignee']))
    task = StoryTask.objects.create(pk=episode.pk,
                                    assigner=request.user,
                                    assignee=assignee,
                                    episode=episode)
    assignee_name = assignee.student_profile.ar_first_name + " " + assignee.student_profile.ar_last_name
    return {"episode_pk": episode.pk,
            "assignee_name": assignee_name}

# --- Articles ---

@login_required
def list_articles(request):
    """
    Show a list of all articles with the different options (for Media Center members).
    Show a list of the user's own submitted articles with their status (for others).
    """
    # --- Permission Checks ---
    # The user should be part of the Media Center (either head or member)
    media_center = get_media_center()
    user_clubs = get_user_clubs(request.user)
    if media_center in user_clubs or request.user.is_superuser:
        # show a list of all articles
        articles = Article.objects.all()
        return render(request, 'media/list_articles.html', {'articles': articles})
    else:
        # show a list of user's articles
        articles = Article.objects.filter(author=request.user)
        return render(request, 'media/list_user_articles.html', {'articles': articles})

@login_required
def submit_article(request):
    """
    Submit an Article.
    """
    if request.method == 'POST':
        form = ArticleForm(request.POST,
                           instance=Article(author=request.user),
                           )
        if form.is_valid():
            article = form.save()
            
            # assign a task to a random MC member to review the article
            article.assignee = random.choice(get_media_center().members.all())
            article.save()
            
            return HttpResponseRedirect(reverse('media:list_articles'))
    else:
        form = ArticleForm()
    return render(request, 'media/article_write.html', {'form': form})
  
@login_required  
def show_article(request, pk):
    """
    Show an article.
    """
    article = get_object_or_404(Article, pk=pk)
    # --- Permission Checks ---
    # Only media center members and the article's author can view
    # the article before it's approved
    if not article.status == 'A':
        if not get_media_center() in get_user_clubs(request.user) \
           and not article.author == request.user:
            raise PermissionDenied
        
    try:
        review = ArticleReview.objects.get(article=article)
        review_form = ArticleReviewForm(instance=review)
    except ObjectDoesNotExist:
        review = None
        review_form = ArticleReviewForm()
    context = {}
    context['article'] = article
    # if the user is a member of the media club plus being the article's
    # assignee, show the review form; otherwise only show the review
    if (get_media_center() in get_user_clubs(request.user) and \
       article.assignee == request.user) or \
       get_media_center().coordinator == request.user:
        context['review_form'] = review_form
    else:
        context['review'] = review
    return render(request, 'media/article_read.html', context)

@login_required
def edit_article(request, pk):
    """
    Edit an article.
    """
    article = get_object_or_404(Article, pk=pk)
    # --- Permission Checks ---
    # Only the article's author should be able to edit it
    # and only when the reviewer asks for an edit
    if not article.author == request.user or not article.status == 'E':
        raise PermissionDenied
    
    try:
        review = ArticleReview.objects.get(article=Article.objects.get(pk=pk))
    except ObjectDoesNotExist:
        review = None
    
    if request.method == 'POST':
        form = ArticleForm(request.POST,
                           instance=article
                           )
        if form.is_valid():
            form.save()
            # update article status
            article.status = 'P' # pending
            article.save()
            return HttpResponseRedirect(reverse('media:show_article',
                                                args=(pk, )))
    else:
        form = ArticleForm(instance=article)
    return render(request, 'media/article_write.html', {'form': form,
                                                        'article': article,
                                                        'review': review})

@login_required
def review_article(request, pk):
    """
    Review an article.
    """
    article = Article.objects.get(pk=pk)
    
    # --- Permission Checks ---
    # Only the article's assignee in addition to the media center's
    # head is allowed to review articles
    if (get_media_center() not in get_user_clubs(request.user) or \
       not article.assignee == request.user) and \
       not get_media_center().coordinator == request.user:
        raise PermissionDenied
    
    try:
        review = ArticleReview.objects.get(article=article)
    except ObjectDoesNotExist:
        review = ArticleReview(reviewer=request.user,
                               article=article)
    if request.method == 'POST':
        form = ArticleReviewForm(request.POST,
                                 instance=review
                                 )
        if form.is_valid():
            form.save()
            
            # update article status
            if form.cleaned_data['approve'] == True:
                article.status = 'A' # approved
            else:
                article.status = 'E' # needs editing
            article.save()
            
            return HttpResponseRedirect(reverse('media:list_articles'))
        else:
            return render(request, 'media/article_read.html', {'article': article,
                                                               'review_form': form})
    else:
        return HttpResponseRedirect(reverse('media:show_article',
                                            args=(pk, ))
                                    )