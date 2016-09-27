# -*- coding: utf-8  -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.views.decorators import csrf

from post_office import mail
import unicodecsv

from activities.models import Activity
from clubs.utils import is_coordinator, is_coordinator_or_member, is_member, is_coordinator_or_deputy, is_deanship_of_students_affairs_coordinator_or_member
from activities.utils import can_view_assessments
from core import decorators
from clubs.forms import DisabledClubForm, ClubForm
from clubs.models import Club
from forms_builder.forms.models import FormEntry
from accounts.utils import get_user_city, get_user_gender

FORMS_CURRENT_APP = "club_forms"

# TODO:
#   * After applying  the data  table with  the new  membership action
#     buttons,  create a  message to  inform the  user about  whatever
#     action was taken regarding their membership. [Osama, Aug 2]

@login_required
def list_clubs(request):
    clubs = Club.objects.visible().current_year()
    if not request.user.is_superuser and \
       not is_deanship_of_students_affairs_coordinator_or_member(request.user):
        clubs = clubs.for_user_gender(request.user).for_user_city(request.user)

    def get_club_points(club):
        return club.get_total_points()
    ordered_clubs = sorted(clubs, key=get_club_points, reverse=True)
    context = {'clubs': ordered_clubs}
    return render(request, 'clubs/list.html', context)

@login_required
def show(request, club_id):
    club = get_object_or_404(Club, pk=club_id)

    # If the user has view_activity perm, is member of presidency, or is club coordinator or member,
    # show all club activities.
    # If user is a deanship reviewer, show only those approved by presidency.
    # If user is none of above (employee, student, or other), show only approved activities

    if is_coordinator_or_member(club, request.user) or \
       request.user.is_superuser:
        activities = club.primary_activity.current_year().filter(is_deleted=False)
    else:
        activities = club.primary_activity.current_year().approved()

    can_edit = is_coordinator(club, request.user) or \
               request.user.has_perm('clubs.change_club')
    can_view_members = is_coordinator_or_deputy(club, request.user) or \
                       request.user.has_perm('clubs.view_members')
    can_view_privileges = is_coordinator(club, request.user) or \
                          request.user.has_perm('clubs.view_deputies')
    can_view_applications = is_coordinator_or_deputy(club, request.user) or \
                            request.user.is_superuser
    context = {'club': club, 'can_edit': can_edit,
               'can_view_members': can_view_members,
               'can_view_applications': can_view_applications,
               'can_view_privileges': can_view_privileges,
               'activities': activities}
    return render(request, 'clubs/show.html', context, current_app='club_forms')

@login_required
@permission_required('clubs.add_club', raise_exception=True)
def create(request):
    if request.method == 'POST':
        # Set the submission_date automatically.
        form = ClubForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('clubs:list'))
        else:
            context = {'form': form}
            return render(request, 'clubs/new.html', context)
    else:
        form = ClubForm()
        context = {'form': form}
        return render(request, 'clubs/new.html', context)

@login_required
def edit(request, club_id):
    exisiting_club = get_object_or_404(Club, pk=club_id)

    # If the user is neither the coordinator, nor has the permission
    # to change activities (i.e. not part of the head of the Student
    # Club), raise a PermissionDenied error.
    if not request.user == exisiting_club.coordinator and \
       not request.user.has_perm('clubs.change_club'):
        raise PermissionDenied

    if request.method == 'POST':
        if request.user == exisiting_club.coordinator:
            modified_club = DisabledClubForm(request.POST,
                                             instance=exisiting_club)
        else:
            modified_club = ClubForm(request.POST, instance=exisiting_club)
        modified_club.save()
        return HttpResponseRedirect(reverse('clubs:show',
                                            args=(club_id,)))
    else:
        exisiting_club = get_object_or_404(Club, pk=club_id)
        if request.user == exisiting_club.coordinator:
            form = DisabledClubForm(instance=exisiting_club)
        else:
            form = ClubForm(instance=exisiting_club)
        context = {'form': form, 'club_id': club_id}
        return render(request, 'clubs/new.html', context)

@login_required
def join(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    context = {'club': club}

    # Make sure the user isn't already a member!
    # NOTE: This is only a superficial protection as the user can simply navigate to the form via the form list or URL
    if is_coordinator_or_member(club, request.user):
        context['error_message'] = 'already_in'
    elif get_user_city(request.user) != club.city:
        context['error_message'] = 'city_error'
    elif get_user_gender(request.user) != club.gender:
        context['error_message'] = 'gender_error'

    # If the club's registration is open, then redirect to the
    # registration form Otherwise, return a message that registration
    # is closed
    if club.registration_is_open():
        reg_form = club.get_registration_form()
        return HttpResponseRedirect(reverse("forms:form_detail",
                                            args=(club.id, reg_form.id),
                                            current_app=FORMS_CURRENT_APP))
    else:
        context['error_message'] = 'closed_membership'

    return render(request, 'clubs/join_error.html', context)


@login_required
def view_application(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if not is_coordinator_or_deputy(club, request.user) and \
       not request.user.is_superuser:
        raise PermissionDenied

    if club.has_registration_form():
        reg_form = club.get_registration_form()
        return HttpResponseRedirect(reverse("forms:form_entries_show",
                                            args=(club.id, reg_form.id),
                                            current_app=FORMS_CURRENT_APP))
    else:
        return render(request, "clubs/view_application_error.html", {"club": club}, current_app=FORMS_CURRENT_APP)

# @login_required
# @csrf.csrf_exempt
# @decorators.ajax_only
@decorators.post_only
def approve_application(request, club_id):
    """
    Add the application's applicant to the application's club.
    Then, delete the application.
    """
    club = get_object_or_404(Club, pk=club_id)
    # --- Permission Checks ---
    # The user should be the application's club coordinator
    if not is_coordinator(club, request.user) and \
       not request.user.is_superuser:
        raise Exception(u"ليس لديك الصلاحيات الكافية للقيام بذلك.")

    # Get the list of selected form entries (list of pk's)
    selected = request.POST.getlist("selected")
    if selected:
        # if request.POST.get("approve"):
        entries = FormEntry.objects.filter(id__in=selected)

        for entry in entries:
            user = entry.submitter
            # Add user to club members, in they're not already in
            if not is_member(club, user):
                club.members.add(user)

        if request.POST.get("approve_and_delete"):
            entries.delete()
    return HttpResponseRedirect(reverse("forms:form_entries_show",
                                        args=(club.id, club.get_registration_form().id),
                                        current_app=FORMS_CURRENT_APP))

@login_required
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def control_privileges(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if not is_coordinator_or_deputy(club, request.user) and \
       not request.user.is_superuser:
        raise PermissionDenied
    role = request.POST.get('role')
    username = request.POST.get('username')
    action = request.POST.get('action')

    if not username or not action or not role:
        raise Exception(u'حدث خطأ!')

    user = User.objects.get(username=username)
    if role == 'deputy':
        current_deputies = club.deputies.all()

        if action == 'set':
            if user in current_deputies:
                raise Exception(u'المستخدم نائب حاليا!')
            else:
                club.deputies.add(user)
        elif action == 'unset':
            if not user in current_deputies:
                raise Exception(u'المستخدم ليس نائبا!')
            else:
                club.deputies.remove(user)
    elif role == 'media_representative':
        current_representatives = club.media_representatives.all()
        if action == 'set':
            if user in current_representatives:
                raise Exception(u'المستخدم ممثل إعلامي حاليا!')
            else:
                club.media_representatives.add(user)
                print "done!"
        elif action == 'unset':
            if not user in current_representatives:
                raise Exception(u'المستخدم ليس ممثلا إعلاميًا!')
            else:
                club.media_representatives.remove(user)
        

@login_required
def view_members(request, club_id):
    """
    View a list of the club's members.
    """
    club = get_object_or_404(Club, pk=club_id)
    if not is_coordinator_or_deputy(club, request.user) and \
       not request.user.has_perm('clubs.view_members'):
        raise PermissionDenied
    return render(request, 'clubs/members.html', {'club': club})

@login_required
def view_privileges(request, club_id):
    """
    View a list of the club's members.
    """
    club = get_object_or_404(Club, pk=club_id)
    if not is_coordinator_or_deputy(club, request.user) and \
       not request.user.has_perm('clubs.view_deputies'):
        raise PermissionDenied
    return render(request, 'clubs/privileges.html', {'club': club})

@login_required
def view_assessments(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if not can_view_assessments(request.user, club):
        raise PermissionDenied

    assessed_primary_activities = Activity.objects.approved().filter(primary_club=club, assessment__isnull=False)
    assessed_secondary_activities = Activity.objects.approved().filter(secondary_clubs=club, assessment__isnull=False)

    context = {'club': club,
               'primary_activities': assessed_primary_activities,
               'secondary_activities': assessed_secondary_activities}
    return render(request, 'clubs/assessments.html', context)
