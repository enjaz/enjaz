from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators import csrf
from django.utils import timezone

from core import decorators
from core.models import StudentClubYear
from post_office import mail
from researchhub.models import Supervisor, Project, SkilledStudent, Domain, Skill
from researchhub.forms import ProjectForm, MemberProjectForm, AddSupervisorForm, EditSupervisorForm, SkilledStudentForm, ConsultationForm, FeedbackForm, EmailForm
from researchhub import utils
from wkhtmltopdf.views import PDFTemplateView

def index(request):
    latest_supervisors = Supervisor.objects.available().order_by("-submission_date")[:10]
    supervisor_count =  Supervisor.objects.undeleted().count()
    latest_projects = Project.objects.shown().order_by("-submission_date")[:10]
    project_count = Project.objects.undeleted().count()
    latest_skills = SkilledStudent.objects.available().order_by("-submission_date")[:10]
    skill_count = SkilledStudent.objects.undeleted().count()
    context = {'latest_projects': latest_projects,
               'latest_supervisors': latest_supervisors,
               'latest_skills': latest_skills,
               'supervisor_count': supervisor_count,
               'project_count': project_count,
               'skill_count': skill_count}
    return render(request, "researchhub/index.html", context)

def indicators(request):
    if not utils.is_researchhub_coordinator_or_member(request.user) and\
       not request.user.is_superuser:
        raise PermissionDenied

def list_projects(request):
    if utils.is_researchhub_coordinator_or_member(request.user) or\
       request.user.is_superuser:
        shown_projects = Project.objects.shown().order_by("-submission_date")
        hidden_projects = Project.objects.hidden().order_by("-submission_date")
        return render(request, "researchhub/list_projects_privileged.html",
                      {'shown_projects': shown_projects,
                       'hidden_projects': hidden_projects})
    else:
        projects = Project.objects.shown().order_by("-submission_date")
        return render(request, "researchhub/list_projects.html",
                      {'projects': projects})

class InvitationView(PDFTemplateView):
    def get_context_data(self, **kwargs):
        context = super(InvitationView, self).get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name')
        return context

@login_required
def submit_consultation(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            email_context = {'user': request.user,
                             'data': form.cleaned_data}
            mail.send([request.user.email],
                       template="researchhub_consultation_submitted_to_user",
                       context=email_context)
            mail.send(["researchhub@enjazportal.com"],
                       template="researchhub_consultation_submitted_to_team",
                       context=email_context,
                       headers={'Reply-to': request.user.email})
            return HttpResponseRedirect(reverse('researchhub:consultation_received'))
    else:
        form = ConsultationForm()
    return render(request, 'researchhub/submit_consultation.html',
                  {'form': form})

@decorators.ajax_only
@login_required
def send_email(request, pk):
    supervisor = get_object_or_404(Supervisor, pk=pk)

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email_context = {'user': request.user,
                             'supervisor': supervisor,
                             'data': form.cleaned_data}
            mail.send([request.user.email],
                       "researchhub@enjazportal.com",
                       template="researchhub_send_email_to_student",
                       context=email_context)
            mail.send([supervisor.user.email],
                       "researchhub@enjazportal.com",
                       bcc="researchhub@enjazportal.com",
                       template="researchhub_send_email_to_supervisor",
                       context=email_context,
                       headers={'Reply-to': request.user.email})
            return {"message": "success"}
    elif request.method == 'GET':
        form = EmailForm()

    context = {'form': form,
                'supervisor': supervisor}
    return render(request, 'researchhub/send_email_form.html', context)

@decorators.ajax_only
@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            email_context = {'user': request.user,
                             'data': form.cleaned_data}
            mail.send([request.user.email],
                       template="researchhub_feedback_submitted_to_user",
                       context=email_context)
            mail.send(["researchhub@enjazportal.com"],
                       template="researchhub_feedback_submitted_to_team",
                       context=email_context,
                       headers={'Reply-to': request.user.email})
            return {"message": "success"}
    elif request.method == 'GET':
        form = FeedbackForm()

    context = {'form': form}
    return render(request, 'researchhub/submit_feedback_form.html', context)


@login_required
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def control_projects(request):
    if not utils.is_researchhub_coordinator_or_member(request.user) and\
       not request.user.is_superuser:
        raise Exception('Permission denied!')
    pk = request.POST.get('pk')
    action = request.POST.get('action')

    if not pk or not action:
        raise Exception('Incomplete request!')

    project = Project.objects.get(pk=pk)

    if action == 'hide':
        if project.is_hidden:
            raise Exception(u'Project is already hidden!')
        else:
            project.is_hidden = True
    elif action == 'show':
        if not project.is_hidden:
            raise Exception(u'Project is already shown!')
        else:
            project.is_hidden = False

    project.save()

@decorators.ajax_only
@login_required
def add_project(request):
    if utils.is_researchhub_coordinator_or_member(request.user) or \
       request.user.is_superuser:
        Form = MemberProjectForm
    else:
        Form = ProjectForm
    if request.method == 'POST':
        current_year = StudentClubYear.objects.get_current()
        instance = Project(submitter=request.user, year=current_year)
        form = Form(request.POST, instance=instance)
        if form.is_valid():
            project = form.save()
            show_project_url = reverse('researchhub:show_project', args=(project.pk,))
            full_url = request.build_absolute_uri(show_project_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = Form()

    context = {'form': form}
    return render(request, 'researchhub/edit_project_form.html', context)

def show_project(request, pk):
    project = get_object_or_404(Project, pk=pk, is_deleted=False)
    return render(request, "researchhub/show_project.html",
                  {'project': project})

@decorators.ajax_only
@login_required
def edit_project(request, pk):
    if utils.is_researchhub_coordinator_or_member(request.user) or \
       request.user.is_superuser:
        Form = MemberProjectForm
    else:
        Form = ProjectForm

    project = get_object_or_404(Project, pk=pk, is_deleted=False)
    if not utils.can_edit_project(request.user, project):
        raise Exception("You cannot edit the project.")

    context = {'project': project}
    if request.method == 'POST':
        form = Form(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            show_project_url = reverse('researchhub:show_project', args=(project.pk,))
            full_url = request.build_absolute_uri(show_project_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = Form(instance=project)

    context['form'] = form
    return render(request, 'researchhub/edit_project_form.html', context)

@login_required
@decorators.ajax_only
@decorators.post_only
@csrf.csrf_exempt
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, is_deleted=False)
    if not utils.can_edit_project(request.user, project):
        raise Exception("You cannot delete the project.")

    project.is_deleted = True
    project.save()
    list_projects_url = reverse('researchhub:list_projects')
    full_url = request.build_absolute_uri(list_projects_url)
    return {"message": "success", "list_url": full_url}

def list_domains(request):
    domains = Domain.objects.all()
    return render(request, "researchhub/list_domains.html",
                      {'domains': domains})

def list_supervisors(request, pk):
    if utils.is_researchhub_coordinator_or_member(request.user) or\
       request.user.is_superuser:
        domain = get_object_or_404(Domain, pk=pk)
        available_supervisors = Supervisor.objects.available().order_by("-submission_date").filter(domain=domain)
        unavailable_supervisors = Supervisor.objects.unavailable().order_by("-submission_date").filter(domain=domain)
        return render(request, "researchhub/list_supervisors_privileged.html",
                      {'available_supervisors': available_supervisors,
                       'unavailable_supervisors': unavailable_supervisors,
                       'domain': domain})
    else:
        domain = get_object_or_404(Domain, pk=pk)
        supervisors = Supervisor.objects.available().order_by("-submission_date").filter(domain=domain)
        context = {'domain': domain, 'supervisors': supervisors}
        return render(request, "researchhub/list_supervisors.html",context)

@login_required
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def control_supervisors(request):
    if not utils.is_researchhub_coordinator_or_member(request.user) and\
       not request.user.is_superuser:
        raise Exception('Permission denied!')
    pk = request.POST.get('pk')
    action = request.POST.get('action')

    if not pk or not action:
        raise Exception('Incomplete request!')

    supervisor = Supervisor.objects.get(pk=pk)

    if action == 'hide':
        if supervisor.is_hidden:
            raise Exception(u'Supervisor is already hidden!')
        else:
            supervisor.is_hidden = True
    elif action == 'show':
        if not supervisor.is_hidden:
            raise Exception(u'Supervisor is already shown!')
        else:
            supervisor.is_hidden = False

    supervisor.save()

@login_required
@decorators.ajax_only
def add_supervisor(request):
    if not utils.is_researchhub_coordinator_or_member(request.user) and\
       not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        current_year = StudentClubYear.objects.get_current()
        instance = Supervisor(year=current_year)
        form = AddSupervisorForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            supervisor = form.save()
            show_supervisor_url = reverse('researchhub:show_supervisor', args=(supervisor.pk,))
            full_url = request.build_absolute_uri(show_supervisor_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = AddSupervisorForm()

    context = {'form': form}
    return render(request, 'researchhub/edit_supervisor_form.html', context)

def show_supervisor(request, pk):
    supervisor = get_object_or_404(Supervisor, pk=pk, is_deleted=False)
    return render(request, "researchhub/show_supervisor.html",
                  {'supervisor': supervisor})

@login_required
@decorators.ajax_only
@decorators.post_only
@csrf.csrf_exempt
def rate_supervisor(request, pk):
    supervisor = get_object_or_404(Supervisor, pk=pk, is_deleted=False)

@login_required
@decorators.ajax_only
def edit_supervisor(request, pk):
    supervisor = get_object_or_404(Supervisor, pk=pk, is_deleted=False)
    if not utils.can_edit_supervisor(request.user, supervisor):
        raise Exception("You cannot edit the supervisor.")

    context = {'supervisor': supervisor}
    if request.method == 'POST':
        form = EditSupervisorForm(request.POST, instance=supervisor)
        if form.is_valid():
            supervisor = form.save()
            show_supervisor_url = reverse('researchhub:show_supervisor', args=(supervisor.pk,))
            full_url = request.build_absolute_uri(show_supervisor_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = EditSupervisorForm(instance=supervisor)

    context['form'] = form
    return render(request, 'researchhub/edit_supervisor_form.html', context)

@login_required
@decorators.ajax_only
@decorators.post_only
@csrf.csrf_exempt
def delete_supervisor(request, pk):
    supervisor = get_object_or_404(Supervisor, pk=pk, is_deleted=False)
    if not utils.can_edit_supervisor(request.user, supervisor):
        raise Exception("You cannot delete the supervisor.")

    supervisor.is_deleted = True
    supervisor.save()
    list_supervisors_url = reverse('researchhub:list_supervisors')
    full_url = request.build_absolute_uri(list_supervisors_url)
    return {"message": "success", "list_url": full_url}

def list_skills(request):
    skilledstudents = SkilledStudent.objects.filter(is_deleted=False).order_by("-submission_date")
    skills = Skill.objects.all()
    context = {'skilledstudents': skilledstudents, 'skills': skills}
    return render(request, "researchhub/list_skills.html", context)

@login_required
@decorators.ajax_only
def add_skill(request):
    if request.method == 'POST':
        current_year = StudentClubYear.objects.get_current()
        instance = SkilledStudent(user=request.user,
                         year=current_year)
        form = SkilledStudentForm(request.POST, instance=instance)
        if form.is_valid():
            skill = form.save()
            show_skill_url = reverse('researchhub:show_skill', args=(skill.pk,))
            full_url = request.build_absolute_uri(show_skill_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = SkilledStudentForm()

    context = {'form': form}
    return render(request, 'researchhub/edit_skill_form.html', context)

def show_skill(request, pk):
    skill = get_object_or_404(SkilledStudent, pk=pk, is_deleted=False)
    return render(request, "researchhub/show_skill.html",
                  {'skill': skill})

@decorators.ajax_only
@login_required
def edit_skill(request, pk):
    skill = get_object_or_404(SkilledStudent, pk=pk, is_deleted=False)
    if not utils.can_edit_skill(request.user, skill):
        raise Exception("You cannot edit the skill.")

    context = {'skill': skill}
    if request.method == 'POST':
        form = SkilledStudentForm(request.POST, instance=skill)
        if form.is_valid():
            skill = form.save()
            show_skill_url = reverse('researchhub:show_skill', args=(skill.pk,))
            full_url = request.build_absolute_uri(show_skill_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = SkilledStudentForm(instance=skill)

    context['form'] = form
    return render(request, 'researchhub/edit_skill_form.html', context)

@login_required
@decorators.ajax_only
@decorators.post_only
@csrf.csrf_exempt
def delete_skill(request, pk):
    skill = get_object_or_404(SkilledStudent, pk=pk, is_deleted=False)
    if not utils.can_edit_skill(request.user, skill):
        raise Exception("You cannot delete the skill.")

    skill.is_deleted = True
    skill.save()
    list_skills_url = reverse('researchhub:list_skills')
    full_url = request.build_absolute_uri(list_skills_url)
    return {"message": "success", "list_url": full_url}
