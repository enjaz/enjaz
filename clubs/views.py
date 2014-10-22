# -*- coding: utf-8  -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators import csrf

from post_office import mail
import unicodecsv
from activities.utils import get_approved_activities
from clubs.utils import is_coordinator, is_coordinator_or_member

from core import decorators
from clubs.forms import MembershipForm, DisabledClubForm, ClubForm
from clubs.models import Club, MembershipApplication

FORMS_CURRENT_APP = "club_forms"

# TODO:
#   * After applying  the data  table with  the new  membership action
#     buttons,  create a  message to  inform the  user about  whatever
#     action was taken regarding their membership. [Osama, Aug 2]

@login_required
def list(request):
    clubs = Club.objects.exclude(english_name="Presidency").exclude(english_name="Media Center")
    context = {'clubs':clubs}
    return render(request, 'clubs/list.html', context)

@login_required
def show(request, club_id):
    club = get_object_or_404(Club, pk=club_id)

    # If the user has view_activity perm, is member of presidency, or is club coordinator or member,
    # show all club activities.
    # If user is a deanship reviewer, show only those approved by presidency.
    # If user is none of above (employee, student, or other), show only approved activities

    if request.user.has_perm('activities.view_activity') or \
       request.user.has_perm('activities.add_presidency_review') or \
       is_coordinator_or_member(club, request.user):
        activities = club.primary_activity.all()

    elif request.user.has_perm('activities.add_deanship_review'):
        activities = club.primary_activity.filter(review__review_type="P", review__is_approved=True)

    else:
        activities = get_approved_activities().filter(primary_club=club)

    # If the user has the view_activity permission, is a member or is
    # the coordinator of the given club, they will be able to see all
    # related activities regardless fo their status.  Otherwise, only
    # see the approved ones.
    # if request.user.is_authenticated() and \
    #    (request.user.has_perm('activities.view_activity') or \
    #     club in request.user.memberships.all() or \
    #     club in request.user.coordination.all()):
    #     activities = club.primary_activity.all() | club.secondary_activity.all()
    # else:
    #     activities = club.primary_activity.filter(review__is_approved=True) |\
    #                  club.secondary_activity.filter(review__is_approved=True)

    can_edit = request.user == club.coordinator or \
               request.user.has_perm('clubs.change_club')
    can_view_members = request.user == club.coordinator or \
                       request.user.has_perm('clubs.view_members')
    can_view_applications = request.user == club.coordinator or \
                            request.user.has_perm('clubs.view_application')
    context = {'club': club, 'can_edit': can_edit,
               'can_view_members': can_view_members,
               'can_view_applications': can_view_applications,
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
        return render(request, 'clubs/join.html', context)

    # If the club's registration is open, then redirect to the registration form
    # Otherwise, return a message that registration is closed
    if club.registration_is_open():
        reg_form = club.get_registration_form()
        return HttpResponseRedirect(reverse("forms:form_detail",
                                            args=(club.id, reg_form.id),
                                            current_app=FORMS_CURRENT_APP))
    else:
        context['error_message'] = 'closed_membership'
        return render(request, 'clubs/join.html', context)


@login_required
def view_application(request, club_id):
    # FIXME: rewrite to be based on forms
    club = get_object_or_404(Club, pk=club_id)
    if not is_coordinator(club, request.user) and \
       not request.user.has_perm('clubs.view_application'):
        raise PermissionDenied

    applications = MembershipApplication.objects.filter(club=club)
    context = {'applications': applications, 'club': club}
    return render(request, 'clubs/view_application.html', context)

# @login_required
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def approve_application(request, club_id):
    """
    Add the application's applicant to the application's club.
    Then, delete the application.
    """
    print request.user
    application = get_object_or_404(MembershipApplication, pk=request.POST['application_pk'])
    # --- Permission Checks ---
    # The user should be the application's club coordinator
    if not is_coordinator(application.club, request.user) and \
       not request.user.has_perm('clubs.view_application'):
        raise Exception(u"ليس لديك الصلاحيات الكافية للقيام بذلك.")

    # Check that the application's applicant isn't a member of
    # the application's club
    if application.user in application.club.members.all():
        # Now this shouldn't happen since the join view already prevents
        # members from accessing the view
        raise Exception(u"هذا المستخدم عضو في النادي أصلًا")

    # If all went OK, add the user to the club and delete the application
    application.club.members.add(application.user)
    application.delete()

    # return {}

# @login_required
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def ignore_application(request, club_id):
    """
    Basically delete the application.
    """
    application = get_object_or_404(MembershipApplication, pk=request.POST['application_pk'])
    # --- Permission Checks ---
    # The user should be the application's club coordinator
    if not is_coordinator(application.club, request.user) and \
       not request.user.has_perm('clubs.view_application'):
        raise Exception(u"ليس لديك الصلاحيات الكافية للقيام بذلك.")

    application.delete()

    # return {}

@login_required
def view_members(request, club_id):
    """
    View a list of the club's members.
    """
    club = get_object_or_404(Club, pk=club_id)
    if not is_coordinator(club, request.user) and \
       not request.user.has_perm('clubs.view_members'):
        raise PermissionDenied
    return render(request, 'clubs/members.html', {'club': club})
    
# TODO: remove this view and the associated url since its function is now done by datatables
@login_required
def download_application(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if not club in request.user.coordination.all() and \
       not request.user.has_perm('clubs.view_application'):
        raise PermissionDenied

    applications = MembershipApplication.objects.filter(club=club)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Applications for Club %s.csv"' % club_id

    writer = unicodecsv.writer(response, encoding='utf-8')
    writer.writerow([u"الاسم", u"البريد", u"ملاحظة"])
    for application in applications:
        if application.user.first_name:
            name = u"%s %s" % (application.user.first_name, application.user.last_name)
        else:
            name = application.user.username
        email = application.user.email
        note = application.note
        writer.writerow([name, email, note])
    return response
