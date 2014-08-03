# -*- coding: utf-8  -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied

from post_office import mail
import unicodecsv

from clubs.forms import MembershipForm, DisabledClubForm, ClubForm
from clubs.models import Club, MembershipApplication

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

    # If the user has the view_activity permission, is a member or is
    # the coordinator of the given club, they will be able to see all
    # related activities regardless fo their status.  Otherwise, only
    # see the approved ones.
    if request.user.is_authenticated() and \
       (request.user.has_perm('activities.view_activity') or \
        club in request.user.memberships.all() or \
        club in request.user.coordination.all()):
        activities = club.primary_activity.all() | club.secondary_activity.all()
    else:
        activities = club.primary_activity.filter(review__is_approved=True) |\
                     club.secondary_activity.filter(review__is_approved=True)

    can_edit = request.user == club.coordinator or \
               request.user.has_perm('clubs.change_club')
    can_view_applications = request.user == club.coordinator or \
                            request.user.has_perm('clubs.view_application')
    context = {'club': club, 'can_edit': can_edit,
               'can_view_applications': can_view_applications,
               'activities': activities}
    return render(request, 'clubs/show.html', context)

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
    if not club.open_membership:
        context = {'error_message': 'closed_membership'}
        return render(request, 'clubs/join.html', context)

    # Make sure that the user hasn't already applied!
    existing_application = MembershipApplication.objects.filter(club=club,
                                                       user=request.user)
    if existing_application:
        context['error_message'] = 'already_applied'
        return render(request, 'clubs/join.html', context)

    # Make sure the user isn't already a member!
    if club in request.user.memberships.all() or\
       club in request.user.coordination.all():
        context['error_message'] = 'already_in'
        return render(request, 'clubs/join.html', context)        

    if request.method == 'POST':
        application = MembershipApplication(club=club, user=request.user)
        form = MembershipForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            view_application_url = reverse('clubs:view_application', args=(club_id,))
            full_url = request.build_absolute_uri(view_application_url)
            email_context = {'club': club, 'user': request.user,
                             'full_url': full_url}
            mail.send([club.coordinator.email],
                      template="club_membership_applied",
                      context=email_context)
            return HttpResponseRedirect(reverse('clubs:join_done',
                                                args=(club_id,)))
        else:
            context['form'] = form
            return render(request, 'clubs/join.html', context)
    else:
        form = MembershipForm()
        context['form'] = form
        return render(request, 'clubs/join.html', context)

@login_required
def view_application(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if not club in request.user.coordination.all() and \
       not request.user.has_perm('clubs.view_application'):
        raise PermissionDenied

    applications = MembershipApplication.objects.filter(club=club)
    context = {'applications': applications, 'club': club}
    return render(request, 'clubs/view_application.html', context)

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
