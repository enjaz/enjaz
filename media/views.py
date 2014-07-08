from django.shortcuts import render

from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from activities.models import Activity
from media.models import FollowUpReport, Story, Article, StoryReview, ArticleReview

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
    return render(request, 'media/list_activities.html', {'activities': activities})

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

@login_required
def submit_report(request, episode_pk):
    """
    Submit a FollowUpReport.
    """
    pass

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