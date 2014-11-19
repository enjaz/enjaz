# -*- coding: utf-8  -*-
import functools
import random

from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.contrib.auth.models import User
from django.core import mail
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.decorators import csrf
from post_office import mail
from activities.utils import get_approved_activities
from clubs.utils import get_media_center, is_coordinator_or_member, is_coordinator_of_any_club, is_member_of_any_club, \
    is_coordinator

from core import decorators
from clubs.models import Club
from activities.models import Activity, Episode
from media.models import FollowUpReport, Story, Article, StoryReview, ArticleReview, StoryTask, CustomTask, TaskComment, \
    WHAT_IF, HUNDRED_SAYS, Poll, PollResponse
from media.forms import FollowUpReportForm, StoryForm, StoryReviewForm, ArticleForm, ArticleReviewForm, TaskForm, \
    TaskCommentForm, PollForm, PollResponseForm, PollChoiceFormSet

# --- Constants and wrapper for polls

WHAT_IF_URL = "whatif"
HUNDRED_SAYS_URL = "100says"

# Keywords
ACTIVE = "active"
UPCOMING = "upcoming"
PAST = "past"

def proper_poll_type(view_func):
    """
    A wrapper to ensure the passed ``poll_type`` is valid, then convert that from a url
    to a poll_type easily understood by the view.
    """
    @functools.wraps(view_func)
    def wrapper(request, poll_type, *args, **kwargs):
        if poll_type == WHAT_IF_URL:
            simple_poll_type = WHAT_IF
        elif poll_type == HUNDRED_SAYS_URL:
            simple_poll_type = HUNDRED_SAYS
        else:
            raise Http404
        return view_func(request, poll_type=simple_poll_type, *args, **kwargs)
    return wrapper

def get_poll_type_url(poll_type):
    """
    Return the appropriate url keyword for the passed poll type.
    """
    if poll_type == WHAT_IF:
        return WHAT_IF_URL
    elif poll_type == HUNDRED_SAYS:
        return HUNDRED_SAYS_URL

# --- Helper functions

def get_user_clubs(user):
    return user.coordination.all() | user.memberships.all()

def is_media_coordinator_or_member(user):
    if not (is_coordinator_or_member(get_media_center(), user) or user.is_superuser):
        raise PermissionDenied
    return True

def is_club_coordinator_or_member(user):
    if not ((is_coordinator_of_any_club(user) or is_member_of_any_club(user)
        and not (is_coordinator_or_member(get_media_center(), user))) or user.is_superuser):
        raise PermissionDenied
    return True

def is_media_or_club_coordinator_or_member(user):
    if not (is_coordinator_of_any_club(user) or is_member_of_any_club(user) or user.is_superuser):
        raise PermissionDenied
    return True
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
@user_passes_test(is_media_coordinator_or_member)
def list_activities(request):
    """
    Show a list of activities, with recently approved ones marked, together with
    the available options of FollowUpReports and Stories.
    """
    # Get all approved activities
    activities = get_approved_activities()
    media_center = get_media_center()
    return render(request, 'media/list_activities.html', {'activities': activities,
                                                          'media_center': media_center})

# --- Follow-up Reports ---

@login_required
@user_passes_test(is_media_coordinator_or_member)
def list_reports(request):
    """
    Show a list of all reports in a single table.
    """
    # Get all reports
    reports = FollowUpReport.objects.all()
    return render(request, 'media/list_reports.html', {'reports': reports})

#@permission_required('add_followupreport')
@login_required
@user_passes_test(is_club_coordinator_or_member)
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
                                  request.FILES,
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
@user_passes_test(is_media_or_club_coordinator_or_member)
def show_report(request, episode_pk):
    """
    Show a FollowUpReport.
    """
    episode = get_object_or_404(Episode, pk=episode_pk)
    report = get_object_or_404(FollowUpReport, episode=episode)
    return render(request, 'media/report_read.html', {'report': report})

# --- Stories ---

@login_required
@user_passes_test(is_media_coordinator_or_member)
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
@user_passes_test(is_media_coordinator_or_member)
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
@user_passes_test(is_media_coordinator_or_member)
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
    # Email the assignee with the task
    mail.send([assignee.email],
              template="story_task_assigned",
              context={"task": task})

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
                           request.FILES,
                           instance=Article(author=request.user),
                           )
        if form.is_valid():
            article = form.save()
            
            # assign a task to a random MC member to review the article
            article.assignee = random.choice(get_media_center().members.all())
            article.save()

            # Email the assignee with the task
            mail.send([article.assignee.email],
                      template="article_task_assigned",
                      context={"article": article})

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
           and not article.author == request.user \
           and not request.user.is_superuser:
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
       get_media_center().coordinator == request.user or \
       request.user.is_superuser:
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
    if (not article.author == request.user or not article.status == 'E') \
       and not request.user.is_superuser:
        raise PermissionDenied
    
    try:
        review = ArticleReview.objects.get(article=Article.objects.get(pk=pk))
    except ObjectDoesNotExist:
        review = None
    
    if request.method == 'POST':
        form = ArticleForm(request.POST,
                           request.FILES,
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
@user_passes_test(is_media_coordinator_or_member)
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
       not get_media_center().coordinator == request.user and \
       not request.user.is_superuser:
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

@login_required
@user_passes_test(is_media_coordinator_or_member)
def list_tasks(request):
    """
    For the media center coordinator, list the tasks for all media center members.
    For media center members, list tasks assigned to them.
    """
    context = {}
    if is_coordinator(get_media_center(), request.user) or request.user.is_superuser:
        context['tasks'] = CustomTask.objects.all()
        context['add_task_form'] = TaskForm()
    else:
        context['tasks'] = CustomTask.objects.filter(assignee=request.user)
    return render(request, 'media/list_tasks.html', context)

@login_required
def create_task(request):
    """
    Create a new task.
    """
    # Only the media center coordinator is allowed to assign tasks
    if not is_coordinator(get_media_center(), request.user) and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == "POST":
        task = TaskForm(request.POST,
                        instance=CustomTask(assigner=request.user))
        if task.is_valid():
            task = task.save()
            mail.send([task.assignee.email],
                  template="customtask_assigned",
                  context={"task": task})
            return HttpResponseRedirect(reverse('media:list_tasks'))
    else:
        task = TaskForm()
    return render(request, 'media/create_task.html', {'task_form': task})

@login_required
@user_passes_test(is_media_coordinator_or_member)
def show_task(request, pk):
    """
    Show the task with the given pk.
    """
    task = get_object_or_404(CustomTask, pk=pk)
    return render(request, 'media/show_task.html', {'task': task,
                                                    'comment_form': TaskCommentForm()})

@login_required
@user_passes_test(is_media_coordinator_or_member)
def edit_task(request, pk):
    """
    Show the edit task form if the request is GET.
    Update the task if the request is POST.
    """
    task = get_object_or_404(CustomTask, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('media:list_tasks'))
    else:
        # just show the edit form
        form = TaskForm(instance=task)
    return render(request, 'media/create_task.html', {'task_form': form})

@login_required
@decorators.post_only
def mark_task_complete(request, pk):
    """
    Mark the passed task as complete.
    This can only be done by the task's assignee.
    """
    task = get_object_or_404(CustomTask, pk=pk)

    if not task.assignee == request.user and not request.user.is_superuser:
        raise PermissionDenied

    task.completed = True
    task.save()

    # TODO: email assigner and the media center coordinators

    return HttpResponseRedirect(reverse('media:show_task',
                                        args=(pk, )))

@login_required
@decorators.post_only
@user_passes_test(is_media_coordinator_or_member)
def add_comment(request, pk):
    """
    Add a comment to the task with given pk.
    """
    task = get_object_or_404(CustomTask, pk=pk)
    comment = TaskCommentForm(request.POST,
                              instance=TaskComment(author=request.user,
                                                   task=task))
    if comment.is_valid():
        # Send email to task assigner, assignee, and all participants in the comment thread,
        # excluding -of course- the comment's author
        comment = comment.save()
        recipients = list(set(
            list(task.taskcomment_set.exclude(author=comment.author).values_list('author__email', flat=True))
            + ([task.assigner.email] if task.assigner != comment.author else [])
            + ([task.assignee.email] if task.assignee != comment.author else [])
        ))
        mail.send(recipients,
                  template="taskcomment_added",
                  context={"comment": comment})
        print recipients
    return HttpResponseRedirect(reverse('media:show_task',
                                        args=(pk, )))

# AJAXy challenge!!!
# polls_home view is the only interface with which users interact (at least non-media-center members).
# All the other views are AJAXy, except the ones with which editors interact.

# The idea is as follows:
# polls home returns only an empty page (probably only contains basic stuff) yet contains ajax code
# The ajax code then communicates with polls_list (probably better via 3 urls eg /polls/active/,
# /past/, /upcoming/ [all ajax]). These urls will return the html to show the lists (which is rendered in some
# intermediate template)
# As for past and upcoming (for privileged users) polls, the list shows collapsed polls; when triggered, they will
# ajaxly communicate with show_poll to get the full title, text, choices of a form
# another call to poll_comment will bring up the list of comments for that poll as well as the commenting form
# As for the active form(s), ajax code will bring up the poll details, as well as the voting form (if any)
# The ajax voting
# code could be either loaded initially or via this ajax request
# Successful submission -> ajax call to poll_results

# TODO: add permission checks to views

@proper_poll_type
@login_required
def polls_home(request, poll_type):
    """
    Return the polls home depending on the poll type.
    The poll home consists of the current active poll, and a list of past polls.
    If the user is an editor, also show unpublished polls and editing options.
    """
    # TODO: show editing options for editors
    # The poll home page consists of "boxes" for its different parts, which are loaded
    # via ajax on page load
    if poll_type == HUNDRED_SAYS:
        title = u"المئة تقول"
        intro = "media/polls/100says_intro.html"
    elif poll_type == WHAT_IF:
        title = u"ماذا لو ...؟"
        intro = "media/polls/what_if_intro.html"
    else:
        raise Http404

    is_editor = is_coordinator_or_member(get_media_center(), request.user) or request.user.is_superuser

    context = {"title": title,
               "intro": intro,
               "is_editor": is_editor,
               "poll_type_url": get_poll_type_url(poll_type),
               }
    return render(request, "media/polls/home.html", context)


@decorators.ajax_only
@proper_poll_type
@login_required
def polls_list(request, poll_type, filter):
    """
    For media center coordinator, deputies, or members: return the full list of polls corresponding to the poll_type.
    For normal users, return current and past polls corresponding to the poll_type.
    The list should be classified into past, active, and upcoming.
    """
    # TODO: show editing options for editors
    if filter == PAST:
        polls = Poll.objects.past().filter(poll_type=poll_type)
        template = "media/polls/list_past.html"
    elif filter == ACTIVE:
        polls = Poll.objects.active().filter(poll_type=poll_type)
        template = "media/polls/list_active.html"
    elif filter == UPCOMING:
        polls = Poll.objects.upcoming().filter(poll_type=poll_type)
        template = "media/polls/list_upcoming.html"
    else:
        raise Http404  # Actually this is already taken care of by the proper_poll_type decorator
    context = {'polls': polls,
               'poll_type_url': get_poll_type_url(poll_type)}
    return render(request, template, context)


@decorators.ajax_only
@proper_poll_type
@login_required
def add_poll(request, poll_type):
    """
    GET: return the poll addition form. If the poll_type is HUNDRED_SAYS, allow addition of choices.
    POST: add a new poll corresponding to the poll_type.
    """
    context = {'poll_type_url': get_poll_type_url(poll_type)}
    if request.method == "POST":
        form = PollForm(request.POST, request.FILES, instance=Poll(poll_type=poll_type, creator=request.user))
        if poll_type == HUNDRED_SAYS:
            choices_formset = PollChoiceFormSet(request.POST)

        if form.is_valid() and (choices_formset.is_valid() if poll_type == HUNDRED_SAYS else True):
            poll = form.save()
            if poll_type == HUNDRED_SAYS:
                choices_formset.instance = poll
                choices_formset.save()

            return {"message": "success"}
        else:
            context['form'] = form
            if poll_type == HUNDRED_SAYS: context['choices_formset'] = choices_formset
            return render(request, "media/polls/edit_poll.html", context)
    else:
        context['form'] = PollForm()
        if poll_type == HUNDRED_SAYS: context['choices_formset'] = PollChoiceFormSet()
        return render(request, "media/polls/edit_poll.html", context)


@decorators.ajax_only
@proper_poll_type
@login_required
def edit_poll(request, poll_type, poll_id):
    """
    GET: return the poll editing form. If the poll_type is HUNDRED_SAYS, allow editing of choices.
    POST: edit the passed poll.
    """
    poll = get_object_or_404(Poll, poll_type=poll_type, pk=poll_id)
    context = {'poll_type_url': get_poll_type_url(poll_type), 'poll': poll}
    if request.method == "POST":
        form = PollForm(request.POST, request.FILES, instance=poll)
        if poll_type == HUNDRED_SAYS:
            choices_formset = PollChoiceFormSet(request.POST, instance=poll)

        if form.is_valid() and (choices_formset.is_valid() if poll_type == HUNDRED_SAYS else True):
            form.save()
            if poll_type == HUNDRED_SAYS:
                choices_formset.save()

            return {"message": "success"}
        else:
            context['form'] = form
            if poll_type == HUNDRED_SAYS: context['choices_formset'] = choices_formset
            return render(request, "media/polls/edit_poll.html", context)
    else:
        context['form'] = PollForm(instance=poll)
        if poll_type == HUNDRED_SAYS: context['choices_formset'] = PollChoiceFormSet(instance=poll)
        return render(request, "media/polls/edit_poll.html", context)



@decorators.ajax_only
@proper_poll_type
@login_required
def delete_poll(request, poll_type, poll_id):
    """
    GET: show confirmation message.
    POST: delete given poll.
    """
    pass


@decorators.ajax_only
@proper_poll_type
@login_required
def show_poll(request, poll_type, poll_id):
    """
    GET: return poll contents (title, text, choices (if any), and image, in addition to voting form (for HUNDRED_SAYS).
    POST: respond to poll (vote on a choice)
    """
    poll = get_object_or_404(Poll, poll_type=poll_type, id=poll_id)
    if request.method == "POST":
        form = PollResponseForm(request.POST, instance=PollResponse(poll=poll, user=request.user))
        if form.is_valid():
            try:
                form.save()
                return {"message": "success"}
            except IntegrityError:
                # An IntegrityError will be raised when a user attempts to vote twice
                # (This constraint is specified in Meta of the PollResponse model)
                return {"message": "already_voted"}
        else:
            return {"message": "invalid_form"}
    else:
        # For hundred-says polls, return the poll & choices in an HTML form for voting
        # For what-if polls, return the poll only
        # In both cases load the comments and commenting form as well
        # TODO: instead of 4 templates, could be reduced to simply 1 (think of it)
        context = {'poll': poll, 'poll_type_url': get_poll_type_url(poll_type)}

        suffix = "100says" if poll.poll_type == HUNDRED_SAYS else "whatif" if poll.poll_type == WHAT_IF else ""
        status = "active" if poll.is_active() else "inactive"

        context['is_editor'] = is_coordinator_or_member(get_media_center(), request.user) or request.user.is_superuser

        # If the poll is a hundred-says poll and is active, then pass the voting form to the context
        if poll.poll_type == HUNDRED_SAYS and poll.is_active():
            context['response_form'] = PollResponseForm(instance=PollResponse(poll=poll))

        return render(request, "media/polls/show_%s_%s.html" % (status, suffix), context)


@decorators.ajax_only
@proper_poll_type
@login_required
def poll_comment(request, poll_type, poll_id):
    """
    GET: return list of comments and commenting form for poll.
    POST: comment on a poll.
    """
    pass


@decorators.ajax_only
@proper_poll_type
@login_required
def poll_results(request, poll_type, poll_id):
    """
    For hundred-says polls, return a results page as a pie chart of votes.
    For non-media center members, this shouldn't be accessible unless the user has already voted.
    """
    pass


@decorators.ajax_only
@proper_poll_type
@login_required
def suggest_poll(request, poll_type):
    """
    GET: return poll suggestion form.
    POST: send suggested poll as an email to media center.
    """
    pass
