# -*- coding: utf-8  -*-
import unicodecsv

from datetime import datetime, timedelta, date

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from activities.models import Activity, Review, Participation, Episode
from clubs.models import Club
from books.models import Book
from niqati.models import Niqati_User

class ActivityForm(ModelForm):
    """A general form, which doesn't include 'Presidency'."""
    queryset = Club.objects.exclude(english_name="Presidency")
    primary_club = ModelChoiceField(queryset=queryset,
                                    label=Activity.primary_club.field.verbose_name,
                                    help_text=Activity.primary_club.field.help_text)
    secondary_clubs = ModelMultipleChoiceField(queryset=queryset,
                                    label=Activity.secondary_clubs.field.verbose_name,
                                    help_text=Activity.secondary_clubs.field.help_text,
                                    required=False)
    episode_count = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = Activity
        fields = ['primary_club', # TODO: primary club is already known (signed in):
                                  # no need to include as field
                  'name','description',
                  'organizers', 'participants',
                  'secondary_clubs', 'inside_collaborators',
                  'outside_collaborators', 'requirements',
                  'collect_participants', 'participant_colleges']

    def __init__(self, *args, **kwargs):
        """
        Dynamically add date, time and location fields based on how many
        Episodes are added in the original form. The number of episodes is
        included as a hidden field with the name episode_count.
        Based on this StackOverflow thread:
        http://stackoverflow.com/questions/6142025/dynamically-add-field-to-a-form
        """
        # If an instance is passed, then store it in the instance variable.
        # This will be used in populating the episode fields when an instance
        # is passed.
        instance = kwargs.get('instance', None)
                
        # Initialize the form
        super(ActivityForm, self).__init__(*args, **kwargs)
        
        # Determine how many episodes there are:
        episode_count = 1 # default value
        # First check if an instance is passed. If true, then get the episode count of that instance
        if instance: episode_count = instance.episode_set.count()
        
        # If data is passed (whether it's for a new activity or editing),
        # set episode_count to the episode count within the data.
        # This may override the value obtained from the instance if there is an update in the episodes
        if self['episode_count'].value(): episode_count = self['episode_count'].value()
        
        # In any case, the episode count should be at least 1
        if episode_count < 1: episode_count = 1
        
        #  Set the value of the hidden field to the episode count
        self.fields['episode_count'].initial = episode_count
        
        # If an instance is passed and is saved (has a pk), load its episodes
        if instance:
            if instance.pk:
                instance_episodes = instance.episode_set.all()
        
        # Now add the custom date, time and location fields
        for i in range(int(episode_count)):
            self.fields['episode_pk{i}'.format(i=i)] = forms.CharField(widget=forms.HiddenInput(), required=False)
            self.fields['start_date{i}'.format(i=i)] = forms.DateField(label='تاريخ البداية')
            self.fields['end_date{i}'.format(i=i)] = forms.DateField(label='تاريخ النهاية')
            self.fields['start_time{i}'.format(i=i)] = forms.TimeField(label='وقت البداية')
            self.fields['end_time{i}'.format(i=i)] = forms.TimeField(label='وقت النهاية')
            self.fields['location{i}'.format(i=i)] = forms.CharField(max_length=128, label='المكان')
            
            # If an instance exists (has a pk), then load the fields with the instance episode values.
            # An IndexError arises when submitting an edit form in which new episodes have been added,
            # since episode_count will increase beyond the lenght of instance_episodes.
            # In this case just leave the new fields empty as they will be filled by the submitted data.
            if instance:
                if instance.pk:
                    try:
                        self.fields['episode_pk{i}'.format(i=i)].initial = instance_episodes[i].pk
                        self.fields['start_date{i}'.format(i=i)].initial = instance_episodes[i].start_date
                        self.fields['end_date{i}'.format(i=i)].initial = instance_episodes[i].end_date
                        self.fields['start_time{i}'.format(i=i)].initial = instance_episodes[i].start_time
                        self.fields['end_time{i}'.format(i=i)].initial = instance_episodes[i].end_time
                        self.fields['location{i}'.format(i=i)].initial = instance_episodes[i].location
                    except IndexError:
                        pass
                    
    def clean(self):
        # Remove spaces at the start and end of all text fields.
        cleaned_data = super(ActivityForm, self).clean()
        for field in cleaned_data:
            if isinstance(cleaned_data[field], unicode):
                cleaned_data[field] = cleaned_data[field].strip()
        
        # Check if end_date is after start_date
        
        return cleaned_data
    
    def save(self, *args, **kwargs):
        # Extract and save the episodes, perform a normal save,
        # and link the episodes to the activity
        
        # First, check how many episodes we have
        episode_count = self.cleaned_data['episode_count']
        new_episodes = []
        
        for i in range(int(episode_count)):
            # Get the details of each episode and store them in an Episode object
            pk = self.cleaned_data.pop('episode_pk{i}'.format(i=i), None)
            start_date = self.cleaned_data.pop('start_date{i}'.format(i=i))
            end_date = self.cleaned_data.pop('end_date{i}'.format(i=i))
            start_time = self.cleaned_data.pop('start_time{i}'.format(i=i))
            end_time = self.cleaned_data.pop('end_time{i}'.format(i=i))
            location = self.cleaned_data.pop('location{i}'.format(i=i))
            
            # If there is a pk, i.e. the episode already exists in the database, just update it
            # Otherwise create a new one
            if pk:
                episode = Episode.objects.get(pk=pk)
                
                episode.start_date = start_date
                episode.end_date = end_date
                episode.start_time = start_time
                episode.end_time = end_time
                episode.location = location
                
                episode.save()
            else:
                episode = Episode(start_date=start_date,
                                  end_date=end_date,
                                  start_time=start_time,
                                  end_time=end_time,
                                  location=location)
                new_episodes.append(episode)
                    
        activity = super(ActivityForm, self).save(*args, **kwargs)
        for episode in new_episodes:
            episode.activity = activity
            episode.save()
            
        return activity            
    
class DirectActivityForm(ActivityForm):
    """A form which has 'Presidency' as an option."""
    queryset = Club.objects.all()
    primary_club = ModelChoiceField(queryset=queryset,
                                    label=Activity.primary_club.field.verbose_name,
                                    help_text=Activity.primary_club.field.help_text)
    secondary_clubs = ModelMultipleChoiceField(queryset=queryset,
                                    label=Activity.secondary_clubs.field.verbose_name,
                                    help_text=Activity.secondary_clubs.field.help_text,
                                    required=False)
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['clubs_notes', 'name_notes', 'description_notes',
                  'datetime_notes', 'requirement_notes',
                  'inside_notes', 'outside_notes',
                  'organizers_notes', 'participants_notes',
                  'is_approved', 'submission_date_notes']

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
        context['niqati_count'] = len(request.user.code_set.all())
        context['latest_entries'] = request.user.code_set.all()[::-1][:5]
        
        # --- books --------
        context['books_count'] = len(Book.objects.all())
        context['my_books_count'] = len(request.user.submissions.all())
        context['latest_books'] = Book.objects.all()[::-1][:5]
        
        return render(request, 'home.html', context) # the dashboard
    else:
        context = {}
        if request.method == 'GET' and 'launch' in request.GET:
            context = {'launch': True}
        return render(request, 'front/home_front.html', context)

def list(request):
    # If the user is part of the head of the Student Club, or part of
    # the Media Center, they should be able to view all activities
    # (i.e. approved, rejected and pending).  Otherwise, a user should
    # only see approved activities and the activities of the clubs
    # they have memberships in (regardless of their status).
    if request.user.is_authenticated():
        template = 'activities_base.html'
    else:
        template = 'front/front_base.html'
    
    if request.user.has_perm('activities.view_activity'):
        if request.GET.get('pending') == "1":
            activities = Activity.objects.filter(review__is_approved=None)
        else:
            activities = Activity.objects.all()
    else:
        approved_activities = Activity.objects.filter(review__is_approved=True)
        if request.user.is_authenticated():
            user_activities = request.user.activity_set.all()
            user_clubs = request.user.memberships.all() | request.user.coordination.all()
            primary_activities = Activity.objects.filter(
                primary_club__in=user_clubs)
            secondary_activities = Activity.objects.filter(
                secondary_clubs__in=user_clubs)
        else:
            user_activities = Activity.objects.none()
            primary_activities = Activity.objects.none()
            secondary_activities = Activity.objects.none()
        activities = approved_activities | user_activities | \
                     primary_activities | secondary_activities

    order = request.GET.get('order')
    if order == 'date':
        sorted_activities = activities.order_by('-date')
    elif order == 'club':
        sorted_activities = activities.order_by('-primary_club')
    else:
        sorted_activities = activities.order_by('-submission_date')

    #Each page of results should have a maximum of 25 activities.
    paginator = Paginator(sorted_activities, 25)
    page = request.GET.get('page')

    try:
        page_activities = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_activities = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_activities = paginator.page(paginator.num_pages)

    context = {'template': template, 'page_activities': page_activities}
    return render(request, 'activities/list.html', context)

@login_required
def show(request, activity_id):
    # If the activity is approved, everyone can see it.  If it is not,
    # only the head of the Student Club, the Media Team, the members
    # of the related clubs and the person who submitted it can see it.
    activity = get_object_or_404(Activity, pk=activity_id)
    
    context = {'activity': activity}
    # The activity object is the only thing that should be in the context  [Saeed, 17 Jun 2014]
    
    if request.user.is_authenticated():
        user_clubs = request.user.memberships.all() | request.user.coordination.all()
        is_coordinator = activity.primary_club in request.user.coordination.all()

#        By definition, the coordinator should have all the below-mentioned
#        permissions; all we need is use {{ perms }} from within the template
#        [Saeed, 17 Jun 2014]
#
#         if request.user.has_perm('activities.change_activity') or \
#            is_coordinator:
#             context['can_edit'] = True
#         if request.user.has_perm('activities.view_participation') or \
#            is_coordinator:
#             context['can_view_participation'] = True
#         if request.user.has_perm('activities.can_view_deanship_review') or \
#            is_coordinator:
#             context['can_view_deanship_review'] = True
#         if request.user.has_perm('activities.can_view_presidency_review') or \
#            is_coordinator:
#             context['can_view_presidency_review'] = True
#
#            Everything related to viewing or adding reviews is now moved to the review
#            view, which is more logical and neat [Saeed, 17 Jun 2014]
#
#             try:
#                 review_p = Review.objects.get(activity=activity,
#                                               review_type='P')
#                 context['review_p'] = review_p
#             except ObjectDoesNotExist:
#                 pass
    else:
        user_clubs = Club.objects.none()

    activity_primary_club = activity.primary_club
    activity_secondary_clubs = activity.secondary_clubs.all()
    activity_clubs = [activity_primary_club] + [club for club in activity_secondary_clubs]

#    Again, everything related to reviews is moved to the review view
#    [Saeed, 17 Jun 2014]
#     
#     # We obtain the deanship review specifically because, really,
#     # that's what matters in determining whether a user can see the
#     # activity.
#     try:
#         review_d = Review.objects.get(activity=activity,
#                                       review_type='D')
#         context['review_d'] = review_d
#     except ObjectDoesNotExist:
#         review_d = False
#     
#    This is redundant, since the Activity model has an is_approved()
#    funtion which can be called directly from the template [Saeed, 17 Jun 2014]
#     try:
#         # The important review here is the deanship's, beacuse that
#         # what would determine whether the activity is accessible.
#         activity_status = review_d
#     except ObjectDoesNotExist:
#         activity_status = False


    # The third test condition, that is:
    #   any([club in activity_clubs for club in user_clubs])
    #  checks if any of the clubs the user is a member of is also
    #  orginizing the activity that the user is trying to see.  If
    #  will be True if any club is one of the organizers and it will
    #  be False if none is.
    if not activity.is_approved() and \
       not request.user.has_perm('activities.view_activity') and \
       not any([club in activity_clubs for club in user_clubs]) and \
       not request.user == activity.submitter:
        raise PermissionDenied

#    We can check for the permissions from within the template [Saeed, 17 Jun 2014]
#     if request.user.has_perm('activities.add_presidency_review') or \
#        request.user.has_perm('activities.add_deanship_review'):
#         context['can_review'] = True

    return render(request, 'activities/show_new.html', context)

@login_required
@permission_required('activities.add_activity', raise_exception=True)
def create(request):
    presidency = Club.objects.get(english_name="Presidency")
    if request.method == 'POST':
        activity = Activity(submitter=request.user)
        if request.user.has_perm('activities.directly_add_activity'):
            form = DirectActivityForm(request.POST, instance=activity)
        else:
            form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form_object = form.save()
            # If the chosen primary_club is the Presidency, make it
            # automatically approved by the deanship.
            if form_object.primary_club == presidency:
                review_object = Review.objects.create(
                    activity=form_object, reviewer=request.user,
                    is_approved=True, review_type='D')
            return HttpResponseRedirect(reverse('activities:list'))
        else:
            context = {'form': form}
            return render(request, 'activities/new.html', context)
    else:
        can_directly_add = request.user.has_perm("activities.directly_add_activity")
        try:
            # It is theoretically true that the user can be a
            # coordinator of more than one single club, but we are not
            # taking that into consideration because it is just not
            # common enough.
            user_club = request.user.coordination.all()[0]
        except IndexError:
            # Make it more user-friendly: if the user is an admin,
            # automatically choose presidency as the default
            # primary_club.
            if can_directly_add:
                user_club = presidency
            else:
                user_club = None

        activity = Activity(primary_club=user_club)
        if request.user.has_perm("activities.directly_add_activity"):
            form = DirectActivityForm(instance=activity)
        else:
            form = ActivityForm(instance=activity)
        context = {'form': form}
        return render(request, 'activities/new.html', context)

@login_required
def edit(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    user_coordination = request.user.coordination.all()
    # We need a QuerySet to combine it with secondary clubs.
    activity_primary_club = Club.objects.filter(
        id=activity.primary_club.id)
    activity_secondary_clubs = activity.secondary_clubs.all()
    activity_clubs = activity_primary_club | activity_secondary_clubs

    # If the user is neither the submitter, nor has the permission to
    # change activities (i.e. not part of the head of the Student
    # Club, or the Media Team), not a coordinator of any of the
    # organizing clubs, raise a PermissionDenied error.
    if not request.user == activity.submitter and \
       not request.user.has_perm('activities.change_activity') and \
       not any([club in activity_clubs for club in user_coordination]):
        raise PermissionDenied

    if request.method == 'POST':        
        modified_activity = ActivityForm(request.POST, instance=activity)
        # Should check that edits are valid before saving
        # TODO: actually edits should be approved first by presidency and deanship
        if modified_activity.is_valid():
            modified_activity.save()
            return HttpResponseRedirect(reverse('activities:show',
                                                args=(activity.pk, ))
                                        )
        else:
            context = {'form': modified_activity, 'activity_id': activity_id,
                       'edit': True}
            return render(request, 'activities/new.html', context)
    else:
        form = ActivityForm(instance=activity)
        context = {'form': form, 'activity_id': activity_id,
                   'activity': activity, 'edit': True}
        return render(request, 'activities/new.html', context)

@login_required
def review(request, activity_id, type=None):
    activity = get_object_or_404(Activity, pk=activity_id)

    # We have two types of reviews: the one that is submitted by the
    # presidency (first), and the one that is done by the deanship.
#     if request.user.has_perm('activities.add_presidency_review'):
#         review_type = 'P'
#     elif request.user.has_perm('activities.add_deanship_review'):
#         review_type = 'D'
#     else:
#         raise PermissionDenied

    if type == None:
        # If the user has any permission (read or write) related to the deanship review,
        # redirect to review/d/. Otherwise, if the user has any permission (read or write)
        # related to the presidency review, redirect to review/p/
        # Otherwise, raise PermissionDenied
        if request.user.has_perm('activities.add_deanship_review') or \
           request.user.has_perm('activities.view_deanship_review'):
            return HttpResponseRedirect(reverse('activities:review_with_type',
                                                args=(activity_id, 'd')))
            
        elif request.user.has_perm('activities.add_presidency_review') or \
             request.user.has_perm('activities.view_presidency_review'):
            return HttpResponseRedirect(reverse('activities:review_with_type',
                                                args=(activity_id, 'p')))
        else:
            raise PermissionDenied
        
    elif type == 'p' or type == 'd':
        review_type = type.upper()
    else:
        raise Http404
    
    # Review Type Full
    rt_full = {'P': 'presidency', 'D': 'deanship'}[review_type]
    
    # Permission checks moved down (GET requests).
    # As for POST, it's not necessary because the permission check will already have
    # been done before serving the form page; in addition, CSRF token will prevent any
    # spam. [Saeed 18 Jun 2014]
    if request.method == 'POST':
        try: # If the review is already there, edit it.
            review_object = Review.objects.get(activity=activity,
                                               review_type=review_type)
        except ObjectDoesNotExist:
            review_object = Review(activity=activity,
                                   reviewer=request.user,
                                   review_type=review_type)
        review = ReviewForm(request.POST, instance=review_object)
        if review.is_valid():
            review.save()
            if review.cleaned_data['is_approved']:
                activity.is_editable = False
                activity.save()
            return HttpResponseRedirect(reverse('activities:show',
                                                args=(activity_id,)))
    else: # if not POST
        # If the user has the permission to add a review of the corresponding type
        # then return the review form page to add or edit the review
        # Else, if if they have the permission to read, then return the review read page
        # Otherwise, raise PermissionDenied
        if request.user.has_perm('activities.add_' + rt_full + '_review'):
            template = 'activities/review_write.html'
            try: # If the review is already there, edit it.
                review_object = Review.objects.get(activity=activity,
                                                   review_type=review_type)
                review = ReviewForm(instance=review_object)
            except ObjectDoesNotExist:
                review = ReviewForm()
                # Note 1: Here, review is a ReviewForm object, because we want to write
        
        elif request.user.has_perm('activities.view_' + rt_full + '_review'):
            template = 'activities/review_read.html'
            try:
                review = Review.objects.get(activity=activity,
                                            review_type=review_type)
                # Note 2: Here, review is a Review object, because we just want to read
            except ObjectDoesNotExist:
                review = None
        else:
            raise PermissionDenied
        
    context = {'activity': activity, 'active_tab': rt_full,
               'review': review, 'review_type': review_type}
    return render(request, template, context)

@login_required
def participate(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    colleges = activity.participant_colleges.all()
    if colleges:
        request.user
    existing_participation = Participation.objects.filter(activity=activity,
                                                       user=request.user)
    context = {'activity': activity}

    if existing_participation:
        context['error_message'] = 'already_applied'
        return render(request, 'activities/participate.html', context)
        
    if request.method == 'POST':
        if request.POST['status'] == '1':
            Participation.objects.create(activity=activity,
                                         user=request.user)
            return HttpResponseRedirect(reverse('activities:participate_done',
                                                args=(activity_id,)))
        else:
            context['error_message'] = 'unknown'
            return render(request, 'activities/participate.html', context)
    else:
        return render(request, 'activities/participate.html', context)

@login_required
def view_participation(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if not activity.primary_club in request.user.coordination.all() and \
       not request.user.has_perm('activities.view_participation'):
        raise PermissionDenied

    participations = Participation.objects.filter(activity=activity)
    context = {'participations': participations, 'activity': activity}
    return render(request, 'activities/view_participations.html', context)

@login_required
def download_participation(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if not activity.primary_club in request.user.coordination.all() and \
       not request.user.has_perm('activities.view_participation'):
        raise PermissionDenied

    participations = Participation.objects.filter(activity=activity)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Participants in Activity %s.csv"' % activity_id

    writer = unicodecsv.writer(response, encoding='utf-8')
    writer.writerow([u"الاسم", u"البريد"])
    for participantion in participations:
        if participantion.user.first_name:
            name = u"%s %s" % (participantion.user.first_name, participantion.user.last_name)
        else:
            name = participantion.user.username
        email = participantion.user.email
        writer.writerow([name, email])
    return response
