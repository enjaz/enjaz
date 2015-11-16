# -*- coding: utf-8  -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.views.decorators import csrf
from django.utils import timezone
from post_office import mail

from accounts.utils import get_user_city, get_user_gender
from core import decorators
from core.models import StudentClubYear
from studentguide import utils
from studentguide.models import GuideProfile, Request, Report, Feedback, Tag
from studentguide.forms import GuideForm, RequestForm, ReportForm, FeedbackForm

@login_required
def index(request):
    guide_count = GuideProfile.objects.current_year().undeleted().count()
    context = {'guide_count': guide_count}
    return render(request, "studentguide/index.html", context)

@login_required
def indicators(request):
    if not utils.is_studentguide_coordinator_or_deputy(request.user) and\
       not request.user.is_superuser:
        raise PermissionDenied

    requests = Request.objects.current_year()
    guides = GuideProfile.objects.current_year()
    reports = Report.objects.current_year()
    feedback = Feedback.objects.current_year()
    context = {'requests': requests,
               'guides': guides,
               'reports': reports,
               'feedback': feedback}
    return render(request, "studentguide/indicators.html", context)

@login_required
def new_student_index(request):
    tags = Tag.objects.filter(guide_profiles__isnull=False).distinct()#.order_by("?")
    # Only show tags currently available for the user's gender
    gender = get_user_gender(request.user)
    if gender:
        tags = tags.filter(guide_profiles__user__common_profile__college__gender=gender)
    return render(request, "studentguide/new_student_index.html",
                  {'tags': tags})

@login_required
def choose_random_guide(request, tag_code_name):
    tag = get_object_or_404(Tag, code_name=tag_code_name)
    if not tag.guide_profiles.exists():
        return Http404
    guide = GuideProfile.objects.current_year().undeleted().for_user_gender(request.user).filter(tags=tag).order_by('?').first()
    return HttpResponseRedirect(reverse('studentguide:show_guide',
                                args=(guide.pk,)))

@login_required
def list_guides(request):
    guides = GuideProfile.objects.current_year().undeleted().for_user_gender(request.user).for_user_city(request.user)
    return render(request, "studentguide/list_guides.html",
                  {'guides': guides})

@login_required
def my_profile(request):
    guide = get_object_or_404(GuideProfile, user=request.user)
    return HttpResponseRedirect(reverse('studentguide:show_guide',
                                args=(guide.pk,)))

@login_required
def requests_to_me(request):
    if utils.has_guide_profile(request.user):
        guide = utils.get_user_guide_profile(request.user)
        return HttpResponseRedirect(reverse('studentguide:list_guide_requests',
                                    args=(guide.pk,)))
    else:
        raise Http404

@login_required
def show_guide(request, guide_pk):
    guide = get_object_or_404(GuideProfile, pk=guide_pk, is_deleted=False)
    return render(request, "studentguide/show_guide.html",
                  {'guide': guide})

@login_required
def list_guide_requests(request, guide_pk=None):
    guide = get_object_or_404(GuideProfile, pk=guide_pk, is_deleted=False)

    if not utils.can_edit_guide(request.user, guide):
        raise PermissionDenied

    return render(request, "studentguide/list_guide_requests.html",
                  {'guide': guide})

#@decorators.ajax_only
@csrf.csrf_exempt
@login_required
def list_request_summaries(request, guide_pk=None):
    source = request.POST.get('source')
    condition = request.POST.get('condition')
    if guide_pk:
        guide = get_object_or_404(GuideProfile, pk=guide_pk, is_deleted=False)

    if source == 'guide':
        if condition == 'pending':
            requests = Request.objects.filter(guide=guide, guide_status="P")\
                                      .exclude(requester_status="C")
        elif condition == 'done':
            requests = Request.objects.filter(guide=guide, guide_status="A")\
                                      .exclude(requester_status="C")
        elif condition == 'rejected':
            requests = Request.objects.filter(guide=guide, guide_status="R")\
                                      .exclude(requester_status="C")
        elif condition == 'canceled':
            requests = Request.objects.filter(guide=guide, requester_status="C")
    elif source == 'requester':
        if condition == 'pending':
            requests = Request.objects.filter(user=request.user, guide_status="P")\
                                      .exclude(requester_status="C")
        elif condition == 'done':
            requests = Request.objects.filter(user=request.user, guide_status="A")\
                                      .exclude(requester_status="C")
        elif condition == 'rejected':
            requests = Request.objects.filter(user=request.user, guide_status="R")\
                                      .exclude(requester_status="C")
        elif condition == 'canceled':
            requests = Request.objects.filter(user=request.user, requester_status="C")

    context = {'requests': requests.order_by("-submission_date"), 'source': source}

    return render(request, "studentguide/partials/list_request_summaries.html",
                  context)

@decorators.ajax_only
@login_required
def add_guide(request):
    if request.method == 'POST':
        current_year = StudentClubYear.objects.get_current()
        instance = GuideProfile(user=request.user, year=current_year)
        form = GuideForm(request.POST, request.FILES, instance=instance)
        if form.is_valid() and not utils.has_guide_profile(request.user):
            guide = form.save()
            show_guide_url = reverse('studentguide:show_guide', args=(guide.pk,))
            full_url = request.build_absolute_uri(show_guide_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = GuideForm()

    context = {'form': form}
    return render(request, 'studentguide/edit_guide_form.html', context)

@decorators.ajax_only
@login_required
def edit_guide(request, guide_pk):
    guide = get_object_or_404(GuideProfile, pk=guide_pk,
                              is_deleted=False)

    if not utils.can_edit_guide(request.user, guide):
        raise Exception(u"لا تستطيع تعديل الكتاب")

    context = {'guide': guide}
    if request.method == 'POST':
        form = GuideForm(request.POST, request.FILES, instance=guide)
        if form.is_valid():
            guide = form.save()
            show_guide_url = reverse('studentguide:show_guide', args=(guide.pk,))
            full_url = request.build_absolute_uri(show_guide_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = GuideForm(instance=guide)

    context['form'] = form
    return render(request, 'studentguide/edit_guide_form.html', context)

@decorators.ajax_only
@decorators.post_only
@login_required
@csrf.csrf_exempt
def delete_guide(request, guide_pk):
    guide = get_object_or_404(GuideProfile, pk=guide_pk,
                              is_deleted=False)
    if not utils.can_edit_guide(request.user, guide):
        raise Exception(u"لا تستطيع حذف المرشد")

    guide.is_deleted = True
    guide.save()
    list_guides_url = reverse('studentguide:list_guides')
    full_url = request.build_absolute_uri(list_guides_url)
    return {"message": "success", "list_url": full_url}

@decorators.ajax_only
@login_required
def add_request(request, guide_pk):
    guide = get_object_or_404(GuideProfile, pk=guide_pk,
                              is_deleted=False)
    if request.method == 'POST':
        instance = Request(user=request.user, guide=guide)
        form = RequestForm(request.POST, instance=instance)
        if form.is_valid():
            guide_request = form.save()
            list_guide_requests_url = reverse('studentguide:list_guide_requests', args=(guide.pk,))
            email_full_url = request.build_absolute_uri(list_guide_requests_url)
            email_context = {'guide': guide,
                             'guide_request': guide_request,
                             'full_url': email_full_url}
            mail.send([guide.user.email],
                      template="guide_request_created_to_guide",
                      context=email_context)

            list_my_requests_url = reverse('studentguide:list_my_requests')
            full_url = request.build_absolute_uri(list_my_requests_url)
            return {"message": "success", "list_url": full_url}
    elif request.method == 'GET':
        form = RequestForm()

    context = {'form': form, 'guide': guide}
    return render(request, 'studentguide/edit_request_form.html', context)

@decorators.ajax_only
@login_required
def edit_request(request, guide_pk, request_pk):
    guide_request = get_object_or_404(Request, guide__pk=guide_pk,
                                      guide__is_deleted=False,
                                      pk=request_pk)

    if not utils.can_edit_request(request.user, guide_request):
        raise Exception(u"لا تستطيع تعديل الكتاب")

    context = {'guide_request': guide_request}
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES, instance=guide_request)
        if form.is_valid():
            guide = form.save()
            show_guide_url = reverse('studentguide:show_guide', args=(guide_request.guide.pk,))
            full_url = request.build_absolute_uri(show_guide_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = RequestForm(instance=guide)

    context['form'] = form
    return render(request, 'studentguide/edit_request_form.html', context)

@login_required
def list_reports(request, guide_pk):
    guide = get_object_or_404(GuideProfile, pk=guide_pk, is_deleted=False)

    if not utils.can_edit_guide(request.user, guide):
        raise PermissionDenied

    reports = Report.objects.filter(guide=guide,
                                    is_deleted=False)
    return render(request, 'studentguide/list_reports.html',
                  {'reports': reports, 'guide': guide})

@decorators.ajax_only
@login_required
def add_report(request, guide_pk):
    guide = get_object_or_404(GuideProfile, pk=guide_pk)

    if not utils.can_edit_guide(request.user, guide):
        raise Exception(u"لا تستطيع رفع تقرير")

    if request.method == 'POST':
        current_year = StudentClubYear.objects.get_current()
        instance = Report(guide=guide)
        form = ReportForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            report = form.save()
            show_report_url = reverse('studentguide:show_report', args=(guide.pk, report.pk))
            full_url = request.build_absolute_uri(show_report_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = ReportForm()

    context = {'form': form, 'guide': guide}
    return render(request, 'studentguide/edit_report_form.html', context)

@decorators.ajax_only
@login_required
def edit_report(request, guide_pk, report_pk):
    report = get_object_or_404(Report, guide__pk=guide_pk, pk=report_pk,
                               is_deleted=False)

    if not utils.can_edit_guide(request.user, report.guide):
        raise Exception(u"لا تستطيع رفع تقرير")

    context = {'report': report}
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            report = form.save()
            show_report_url = reverse('studentguide:show_report', args=(report.guide.pk, report.pk))
            full_url = request.build_absolute_uri(show_report_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = ReportForm(instance=report)

    context['form'] = form
    return render(request, 'studentguide/edit_report_form.html', context)

@decorators.ajax_only
@decorators.post_only
@login_required
@csrf.csrf_exempt
def delete_report(request, guide_pk, report_pk):
    report = get_object_or_404(Report, guide__pk=guide_pk,
                               pk=report_pk, is_deleted=False)

    if not utils.can_edit_guide(request.user, report.guide):
        raise Exception(u"لا تستطيع حذف المرشد")

    report.is_deleted = True
    report.save()
    list_reports_url = reverse('studentguide:list_reports',
                               args=(report.guide.pk,))
    full_url = request.build_absolute_uri(list_reports_url)
    return {"message": "success", "list_url": full_url}

@login_required
def show_report(request, guide_pk, report_pk):
    report = get_object_or_404(Report, guide__pk=guide_pk,
                               pk=report_pk, is_deleted=False)

    if not utils.can_edit_guide(request.user, report.guide):
        raise PermissionDenied

    return render(request, "studentguide/show_report.html",
                  {'report': report})

@decorators.ajax_only
@login_required
def add_feedback(request, guide_pk):
    guide = get_object_or_404(GuideProfile, pk=guide_pk)

    if request.method == 'POST':
        instance = Feedback(guide=guide, submitter=request.user)
        form = FeedbackForm(request.POST, instance=instance)
        if form.is_valid():
            feedback = form.save()
            show_feedback_url = reverse('studentguide:show_feedback', args=(guide.pk, feedback.pk))
            full_url = request.build_absolute_uri(show_feedback_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = FeedbackForm()

    context = {'form': form, 'guide': guide}
    return render(request, 'studentguide/edit_feedback_form.html', context)

@login_required
def show_feedback(request, guide_pk, feedback_pk):
    feedback = get_object_or_404(Feedback, guide__pk=guide_pk,
                                 pk=feedback_pk)

    if not utils.is_studentguide_coordinator_or_deputy(request.user) and\
       not request.user.is_superuser and \
       feedback.submitter != request.user:
        raise PermissionDenied

    return render(request, "studentguide/show_feedback.html",
                  {'feedback': feedback})

@decorators.ajax_only
@decorators.post_only
@login_required
@csrf.csrf_exempt
def control_request(request):
    action = request.POST.get('action')
    request_pk = request.POST.get('pk')
    guide_request = get_object_or_404(Request, pk=request_pk)
    guide = guide_request.guide

    email_context = {'guide': guide,
                     'guide_request': guide_request}

    if action.startswith('guide_'):
        if not guide.user == request.user and\
           not user.is_superuser and\
           not utils.is_studentguide_coordinator_or_deputy(request.user):
            raise Exception(u"لا يمكنك اتخاذ إجراء باسم المرشد الطلابي.")
        if action == 'guide_accepted':
            guide_request.guide_status = 'A'
            guide_request.guide_status_date = timezone.now()
            list_my_requests_url = reverse('studentguide:list_my_requests')
            full_url = request.build_absolute_uri(list_my_requests_url)
            email_context['full_url'] = full_url
            mail.send([guide_request.user.email],
                      template="guide_request_accepted_to_requester",
                      context=email_context)

        elif action == 'guide_rejected':
            guide_request.guide_status = 'R'
            guide_request.guide_status_date = timezone.now()
            new_student_index_url = reverse('studentguide:new_student_index')
            full_url = request.build_absolute_uri(new_student_index_url)
            email_context['full_url'] = full_url
            mail.send([guide_request.user.email],
                      template="guide_request_rejected_to_requester",
                      context=email_context)

    elif action.startswith('requester_'):
        if guide_request.user != request.user:
            raise Exception(u"لا يمكنك اتخاذ إجراء باسم مقدم الطلب.")

        if action == 'requester_canceled':
            guide_request.requester_status = 'C'
            guide_request.requester_status_date = timezone.now()
            list_guide_requests_url = reverse('studentguide:list_guide_requests', args=(guide.pk,))
            full_url = request.build_absolute_uri(list_guide_requests_url)
            email_context['full_url'] = full_url
            mail.send([guide.user.email],
                      template="guide_request_canceled_to_guide",
                      context=email_context)

    guide_request.save()
    guide.update_availability_status()
    guide.save()    
    return {"message": "success"}
