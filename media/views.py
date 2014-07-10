from django.shortcuts import render

from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from clubs.models import Club
from activities.models import Activity, Episode
from media.models import FollowUpReport, Story, Article, StoryReview, ArticleReview
from media.forms import FollowUpReportForm

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
    media_center = Club.objects.get(english_name="Media Center")
    return render(request, 'media/list_activities.html', {'activities': activities,
                                                          'media_center': media_center})

@login_required
def list_reports(request):
    """
    Show a list of all reports in a single table.
    """
    # Get all reports
    reports = FollowUpReport.objects.all()
    return render(request, 'media/list_reports.html', {'reports': reports})

@login_required
def list_articles(request):
    """
    Show a list of all articles with the different options (for Media Center members).
    Show a list of the user's own submitted articles with their status (for others).
    """
    pass

#@permission_required('add_followupreport')
@login_required
def submit_report(request, episode_pk):
    """
    Submit a FollowUpReport.
    """
    try:
        episode = Episode.objects.get(pk=episode_pk)
    except ObjectDoesNotExist:
        raise Http404
    
    # Permission checks
    # (1) The passed episode should be owned by the user's club
    user_clubs = request.user.coordination.all() | request.user.memberships.all()
    if episode.activity.primary_club not in user_clubs and not request.user.is_superuser:
        raise PermissionDenied
    # (2) The passed episode shouldn't already have an episode.
    #     Overriding a previous submission shouldn't be allowed
    try:
        report = episode.followupreport
        raise PermissionDenied
    except ObjectDoesNotExist:
        pass
    
    if request.method == 'POST':
        form = FollowUpReportForm(request.POST,
                                  instance=FollowUpReport(episode=episode,
                                                          submitter=request.user)
                                  )
        if form.is_valid():
            # FIXME: missing model fields
            form.save()
            return HttpResponseRedirect(reverse('media:index'))
    else:
        # Initialize the form with initial data from the episode
        form = FollowUpReportForm(initial={'start_date' : episode.start_date,
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
def show_report(request, pk):
    """
    Show a FollowUpReport.
    """
    pass

@login_required
def submit_story(request, episode_pk):
    """
    Submit a Story.
    """
    pass

@login_required
def show_story(request, pk):
    """
    Show a Story.
    """
    pass

@login_required
def review_story(request, pk):
    """
    Review a Story by writing notes or editing it directly.
    """
    pass

@login_required
def submit_article(request):
    """
    Submit an Article.
    """
    pass
  
@login_required  
def show_article(request, pk):
    """
    Show an article.
    """
    pass

@login_required
def edit_article(request, pk):
    """
    Edit an article.
    """
    pass

@login_required
def review_article(request, pk):
    """
    Review an article.
    """
    pass