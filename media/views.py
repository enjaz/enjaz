# -*- coding: utf-8  -*-
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

from clubs.utils import get_media_center,  is_member_of_any_club, \
                        has_coordination_to_activity, \
                        is_employee_of_any_club, get_user_clubs
from core import decorators
from clubs.models import Club
from activities.models import Activity, Episode
from media.models import FollowUpReport, Story, Article, StoryReview, ArticleReview, StoryTask, CustomTask, TaskComment, \
    WHAT_IF, HUNDRED_SAYS, Poll, PollResponse, PollComment, POLL_TYPE_CHOICES, ReportComment, Buzz
from media.forms import FollowUpReportForm, StoryForm, StoryReviewForm, ArticleForm, ArticleReviewForm, TaskForm, \
    TaskCommentForm, PollForm, PollResponseForm, PollChoiceFormSet, PollCommentForm, PollSuggestForm, \
    FollowUpReportImageFormset, ReportCommentForm, BuzzForm
from media.utils import is_media_coordinator_or_member, is_club_coordinator_or_member, is_media_or_club_coordinator_or_member, proper_poll_type, get_poll_type_url, media_coordinator_or_member_test, get_user_media_center, get_clubs_for_media_center

# Keywords
ACTIVE = "active"
UPCOMING = "upcoming"
PAST = "past"

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
@user_passes_test(media_coordinator_or_member_test)
def list_activities(request):
    """
    Show a list of activities, with recently approved ones marked, together with
    the available options of FollowUpReports and Stories.
    """
    media_center = get_user_media_center(request.user)
    if media_center:
        clubs = get_clubs_for_media_center(media_center)
    else:
        # For superuser, show them all.
        clubs = Club.objects.current_year().visible()
    return render(request, 'media/list_activities.html', {'clubs': clubs})

# --- Follow-up Reports ---

@login_required
@user_passes_test(media_coordinator_or_member_test)
def list_reports(request):
    """
    Show a list of all reports in a single table.
    """
    # Get all reports
    media_center = get_user_media_center(request.user)
    if media_center:
        clubs = get_clubs_for_media_center(media_center)
    else:
        # For superuser, show them all.
        clubs = Club.objects.current_year().visible()

    reports = FollowUpReport.objects.current_year().filter(episode__activity__primary_club__in=clubs)
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
    # (1) The user should be part of the primary or secondary club(s) owning the activity
    if not has_coordination_to_activity(request.user, episode.activity) and not request.user.is_superuser:
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
        image_formset = FollowUpReportImageFormset(request.POST, request.FILES)
        if form.is_valid() and image_formset.is_valid():
            instance = form.save()
            image_formset.instance = instance
            image_formset.save()

            # If there is an MC member assigned to write a story for the passed episode, notify them that
            # the report has been submitted
            try:
                task = episode.storytask

                mail.send([task.assignee.email],
                          template="media_report_submit",
                          context={"report": instance, "task": task})
            except ObjectDoesNotExist:
                pass

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
        image_formset = FollowUpReportImageFormset()
    return render(request, 'media/report_write.html', {'form': form,
                                                       'image_formset': image_formset,
                                                       'episode': episode})

@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
@login_required
def update_report_options(request):
    """
    Update report options for a particular episode.
    There 2 options: whether a report is required, and whether a report can be submitted early.
    """
    media_center = get_media_center()
    # Permission checks
    # The user should be the coordinator or deputy of the media center
    if not is_media_coordinator_or_member(request.user) and not request.user.is_superuser:
        raise PermissionDenied

    episode = get_object_or_404(Episode, pk=request.POST['episode_pk'])

    # Update option
    action = request.POST['action']
    if action == "exempt-report":
        episode.requires_report = False
        episode.save()

        mail.send([episode.activity.primary_club.coordinator.email],
                  cc=[media_center.email],
                  template="media_report_exempted",
                  context={"episode": episode})

    elif action == "cancel-exempt-report":
        episode.requires_report = True
        episode.save()

        mail.send([episode.activity.primary_club.coordinator.email],
                  cc=[media_center.email],
                  template="media_report_exempt_cancel",
                  context={"episode": episode})

    elif action == "allow-early-report":
        episode.can_report_early = True
        episode.save()

        mail.send([episode.activity.primary_club.coordinator.email],
                  cc=[media_center.email],
                  template="media_early_report_allowed",
                  context={"episode": episode})

    elif action == "cancel-allow-early-report":
        episode.can_report_early = False
        episode.save()

        mail.send([episode.activity.primary_club.coordinator.email],
                  cc=[media_center.email],
                  template="media_early_report_cancel",
                  context={"episode": episode})

    # Email notifications

    # Return updated button
    return render(request, "media/components/report_options.html", {"episode": episode,
                                                                    "media_center": media_center})

@login_required
def show_report(request, episode_pk):
    """
    Show a FollowUpReport.
    """
    episode = get_object_or_404(Episode, pk=episode_pk)
    report = get_object_or_404(FollowUpReport, episode=episode)

    # Permission checks

    # The passed episode should be owned by the user's club, the user
    # should be a member of the media center, or the user needs to be
    # an employee.
    if not has_coordination_to_activity(request.user, episode.activity) \
       and not is_media_coordinator_or_member(request.user) \
       and not request.user.is_superuser \
       and not is_employee_of_any_club(request.user):
        raise PermissionDenied

    return render(request, 'media/report_read.html', {'report': report, 'comment_form': ReportCommentForm()})

@login_required
@user_passes_test(is_media_or_club_coordinator_or_member)
def edit_report(request, episode_pk):
    episode = get_object_or_404(Episode, pk=episode_pk)
    report = get_object_or_404(FollowUpReport, episode=episode)

    # Permission checks
    # The passed episode should be owned by the user's club or the user should be a member of the media center
    # This is more specific than the test of ``user_passes_test`` above.
    if not has_coordination_to_activity(request.user, episode.activity)\
            and not is_media_coordinator_or_member(request.user) \
            and not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        form = FollowUpReportForm(request.POST, instance=report)
        image_formset = FollowUpReportImageFormset(request.POST, request.FILES, instance=report)
        if form.is_valid() and image_formset.is_valid():
            form.save()
            image_formset.save()

            # Send notification to media center
            mail.send([get_media_center().email],
                      template="media_edit_report",
                      context={"report": report})

            return HttpResponseRedirect(reverse('media:show_report',
                                                args=(episode.pk, )
                                                ))
    else:
        form = FollowUpReportForm(instance=report)
        image_formset = FollowUpReportImageFormset(instance=report)
        return render(request, "media/report_write.html", {'form': form,
                                                           'image_formset': image_formset,
                                                           'episode': episode,
                                                           'edit': True})

@decorators.post_only
@login_required
@user_passes_test(is_media_or_club_coordinator_or_member)
def report_comment(request, episode_pk):
    episode = get_object_or_404(Episode, pk=episode_pk)
    report = get_object_or_404(FollowUpReport, episode=episode)

    # Permission checks
    # The passed episode should be owned by the user's club or the user should be a member of the media center
    # This is more specific than the test of ``user_passes_test`` above.
    if not has_coordination_to_activity(request.user, episode.activity)\
            and not is_media_coordinator_or_member(request.user) \
            and not request.user.is_superuser:
        raise PermissionDenied

    comment_form = ReportCommentForm(request.POST, instance=ReportComment(report=report, author=request.user))

    if comment_form.is_valid():
        comment = comment_form.save()

        # Send email notifications to the report submitter (& the coordinator if they are different),
        # in addition to the media center email plus all participants in the thread.
        # In any case, of course, the author is excluded.
        coordinator = report.episode.activity.primary_club.coordinator
        recipients = list(set(
            list(report.comments.exclude(author=request.user).values_list('author__email', flat=True))
            + ([report.submitter.email] if not request.user == report.submitter else [])
            + ([coordinator.email] if (report.submitter != coordinator and request.user != coordinator) else [])
            + ([get_media_center().email])
        ))

        for recipient in recipients:
            mail.send([recipient],
                      template="media_report_comment",
                      context={"report": report, "comment": comment})

    return HttpResponseRedirect(reverse("media:show_report", args=(episode.pk, )))

# --- Stories ---

@login_required
@user_passes_test(media_coordinator_or_member_test)
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
            story = form.save()
            # TODO: resolve task

            # Send a notification to the media center email
            mail.send([get_media_center().email],
                      template="media_story_created",
                      context={"story": story})

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
@user_passes_test(media_coordinator_or_member_test)
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
@user_passes_test(media_coordinator_or_member_test)
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
    # FIXME: coordinator or deputy
    
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

    assignee_name = assignee.common_profile.ar_first_name + " " + assignee.common_profile.ar_last_name
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
@user_passes_test(media_coordinator_or_member_test)
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
@user_passes_test(media_coordinator_or_member_test)
def list_tasks(request):
    """
    For the media center coordinator, list the tasks for all media center members.
    For media center members, list tasks assigned to them.
    """
    context = {}
    if is_media_coordinator_or_member(request.user) or request.user.is_superuser:
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
    if not is_media_coordinator_or_member(request.user) and not request.user.is_superuser:
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
@user_passes_test(media_coordinator_or_member_test)
def show_task(request, pk):
    """
    Show the task with the given pk.
    """
    task = get_object_or_404(CustomTask, pk=pk)
    return render(request, 'media/show_task.html', {'task': task,
                                                    'comment_form': TaskCommentForm()})

@login_required
@user_passes_test(media_coordinator_or_member_test)
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
@user_passes_test(media_coordinator_or_member_test)
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


@proper_poll_type
@login_required
def polls_home(request, poll_type):
    """
    Return the polls home depending on the poll type.
    The poll home consists of the current active poll, and a list of past polls.
    If the user is an editor, also show unpublished polls and editing options.
    """
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

    is_editor = is_media_coordinator_or_member(request.user) or request.user.is_superuser

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
    # TODO: reduce templates into list_active and list_inactive
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
@decorators.post_only
@proper_poll_type
@login_required
def delete_poll(request, poll_type, poll_id):
    """
    GET: show confirmation message.
    POST: delete given poll.
    """
    poll = get_object_or_404(Poll, poll_type=poll_type, pk=poll_id)
    poll.delete()
    return {"message": "success"}


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
        context = {'poll': poll, 'poll_type_url': get_poll_type_url(poll_type)}

        context['is_active'] = poll.is_active()
        context['has_choices'] = poll.poll_type == HUNDRED_SAYS
        context['is_editor'] = is_media_coordinator_or_member(request.user) or request.user.is_superuser
        context['has_voted'] = poll.responses.filter(user=request.user).exists()

        # If the poll is a hundred-says poll and is active, then pass the voting form to the context
        if poll.poll_type == HUNDRED_SAYS and poll.is_active():
            context['response_form'] = PollResponseForm(instance=PollResponse(poll=poll))

        return render(request, "media/polls/show_poll.html", context)


@decorators.ajax_only
@proper_poll_type
@login_required
def poll_comment(request, poll_type, poll_id):
    """
    GET: return list of comments and commenting form for poll.
    POST: comment on a poll.
    """
    poll = get_object_or_404(Poll, poll_type=poll_type, pk=poll_id)
    context = {"poll": poll,
               "poll_type_url": get_poll_type_url(poll_type),
               "is_editor": is_media_coordinator_or_member(request.user) or request.user.is_superuser,
               'comments': poll.comments.all()}
    if request.method == "POST":
        comment_form = PollCommentForm(request.POST, instance=PollComment(poll=poll, author=request.user))
        if comment_form.is_valid():
            comment_form.save()
            return {"message": "success"}
        else:
            context["comment_form"] = comment_form
            return render(request, "media/polls/comments.html", context)
    else:
        if poll.is_active():
            context['comment_form'] = PollCommentForm()
        return render(request, "media/polls/comments.html", context)
    # TODO: only show part (1st 3) of the comments list at first


@decorators.ajax_only
@decorators.post_only
@proper_poll_type
@user_passes_test(media_coordinator_or_member_test)
@login_required
def delete_poll_comment(request, poll_type, poll_id):
    poll = get_object_or_404(Poll, poll_type=poll_type, pk=poll_id)
    comment_id = request.POST['comment_id']
    comment = get_object_or_404(PollComment, poll=poll, pk=comment_id)
    comment.delete()
    return {"message": "success"}


@decorators.ajax_only
@proper_poll_type
@login_required
def poll_results(request, poll_type, poll_id):
    """
    For hundred-says polls, return a results page as a pie chart of votes.
    For non-media center members, this shouldn't be accessible unless the user has already voted.
    """
    poll = get_object_or_404(Poll, poll_type=poll_type, pk=poll_id)

    # Make sure it's a HUNDRED_SAYS poll
    assert poll.poll_type == HUNDRED_SAYS

    # The poll should be inactive or the
    # user should either be an editor or has voted in order to be allowed to see the results
    has_voted = poll.responses.filter(user=request.user).exists()
    if poll.is_active() and not has_voted and not (request.user.is_superuser or is_media_coordinator_or_member(user)):
        raise PermissionDenied

    return render(request, "media/polls/results.html", {"poll": poll, "poll_type_url": get_poll_type_url(poll_type)})


@decorators.ajax_only
@proper_poll_type
@login_required
def suggest_poll(request, poll_type):
    """
    GET: return poll suggestion form.
    POST: send suggested poll as an email to media center.
    """
    poll_type_url = get_poll_type_url(poll_type)
    poll_type_name = dict(POLL_TYPE_CHOICES)[poll_type]
    if request.method == "POST":
        form = PollSuggestForm(poll_type, request.POST)
        if form.is_valid():
            context = dict()
            # extract the fields and prepare the context
            context['title'] = form.cleaned_data['title']
            context['text'] = form.cleaned_data['text']
            if poll_type == HUNDRED_SAYS:
                context['choices'] = form.cleaned_data['choices']

            context['poll_type_name'] = poll_type_name

            # email the suggestion
            mail.send([get_media_center().email],
                      template="media_poll_suggestion",
                      context=context)
            return {"message": "success"}
        else:
            return render(request, "media/polls/suggest.html", {"form": form,
                                                                "poll_type_url": poll_type_url,
                                                                "poll_type_name": poll_type_name})

    else:
        form = PollSuggestForm(poll_type)
        return render(request, "media/polls/suggest.html", {"form": form,
                                                            "poll_type_url": poll_type_url,
                                                            "poll_type_name": poll_type_name})


# What's New?
@login_required
@user_passes_test(media_coordinator_or_member_test)
def buzzes_home(request):
    """
    Return the buzzes home
    The buzz home consists of the current published buzz, and a list of upcoming buzzes.
    """
    # The buzz home page consists of "boxes" for its different parts, which are loaded
    # via ajax on page load

    return render(request, "media/buzzes/home.html")


@decorators.ajax_only
@login_required
@user_passes_test(media_coordinator_or_member_test)
def buzzes_list(request, list_filter):
    """
    For media center coordinator, deputies, or members: return the full list of buzzes.
    The list should be classified into published, and upcoming.
    """
    if list_filter == ACTIVE:
        buzzes = Buzz.objects.published()
        template = "media/buzzes/list_published.html"
    elif list_filter == UPCOMING:
        buzzes = Buzz.objects.upcoming()
        template = "media/buzzes/list_upcoming.html"
    context = {'buzzes': buzzes}
    return render(request, template, context)


@decorators.ajax_only
@login_required
@user_passes_test(media_coordinator_or_member_test)
def add_buzz(request):
    """
    GET: return the buzz addition form.
    POST: add a new buzz
    """
    if request.method == "POST":
        form = BuzzForm(request.POST, request.FILES, instance=Buzz(submitter=request.user))

        if form.is_valid():
            buzz = form.save()
            return {"message": "success"}
        else:
            context = {'form': form}
    else:
        context = {'form': BuzzForm()}
    return render(request, "media/buzzes/edit_buzz.html", context)

@decorators.ajax_only
@login_required
@user_passes_test(media_coordinator_or_member_test)
def edit_buzz(request, buzz_id):
    """
    GET: return the buzz editing form.
    POST: edit the passed buzz.
    """
    buzz = get_object_or_404(Buzz, pk=buzz_id)
    context = {'buzz': buzz}
    if request.method == "POST":
        form = BuzzForm(request.POST, request.FILES, instance=buzz)

        if form.is_valid():
            form.save()
            return {"message": "success"}
        else:
            context['form'] = form
    else:
        context['form'] = BuzzForm(instance=buzz)
    return render(request, "media/buzzes/edit_buzz.html", context)

@decorators.ajax_only
@login_required
@user_passes_test(media_coordinator_or_member_test)
def show_buzz(request, buzz_id):
    """
    GET: return buzz contents (title, text, and image)
    """
    buzz = get_object_or_404(Buzz, id=buzz_id)
    context = {'buzz': buzz}
    return render(request, "media/buzzes/show_buzz.html", context)

@decorators.ajax_only
@decorators.post_only
@login_required
@user_passes_test(media_coordinator_or_member_test)
def delete_buzz(request, buzz_id):
    """
    GET: show confirmation message.
    POST: delete given poll.
    """
    buzz = get_object_or_404(Buzz, pk=buzz_id)
    buzz.is_deleted=True
    buzz.save()
    return {"message": "success"}
