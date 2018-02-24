from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from matching_program import utils
from models import ResearchProject, StudentApplication
from matching_program.forms import ResearchProjectForm, StudentApplicationForm


@login_required
def index(request):
    new_projects = ResearchProject.objects.filter(status="N")
    inProgress_projects = ResearchProject.objects.filter(status="IP")
    puplished_projects = ResearchProject.objects.filter(status="P")
    context= {"new_projects":new_projects,"inProgress_projects":inProgress_projects,
              "puplished_projects":puplished_projects}
    
    if utils.is_matchingProgram_coordinator_or_member(request.user) or\
       request.user.is_superuser:
        applied_projects = ResearchProject.objects.filter(status="A")
        context['applied_projects']=applied_projects
        
    return render(request, "matching_program/index.html",
                  context)

def add_project(request):
    if request.method == 'POST':
        Project = ResearchProject(creator= request.user)
        form = ResearchProjectForm(request.POST, instance= Project)
        if form.is_valid():
            form_object = form.save()
            return HttpResponseRedirect(reverse('matching_program:index'))
    return render(request, "matching_program/edit_project_form.html",
                  {"form":ResearchProjectForm})
    
@login_required
def project(request,pk):
    project= ResearchProject.objects.get(id=pk)
    context={'project':project, 'form': StudentApplicationForm}

    if utils.is_matchingProgram_coordinator_or_member(request.user) or\
       request.user.is_superuser:
        members = project.members.all
        print members
        applications= StudentApplication.objects.filter(research__id=pk).exclude(user__in=members)
        context['applications']= applications
        
    if request.method == 'POST':
        Application = StudentApplication(user= request.user, research= project)
        form= StudentApplicationForm(request.POST, instance= Application)
        if form.is_valid():
            form_object= form.save()
    return render(request, "matching_program/project.html",
                  context)
        
def edit_project(request, pk):
    project= ResearchProject.objects.get(id=pk)
    if request.method == "POST":
        ResearchProject.update_project(project, request)
        return HttpResponseRedirect(reverse('matching_program:project',kwargs={"pk":pk}))
    return render(request, "matching_program/edit_project_form.html",
                  {'form':ResearchProjectForm(instance=project), "pk":pk})

def delete_project(request,pk):
    project = ResearchProject.objects.get(id=pk)
    project.delete()
    return HttpResponseRedirect(reverse('matching_program:index'))

def add_member(request,pk):
    student = StudentApplication.objects.get(id=pk)
    project = student.research
    project.members.add(student.user)
    project.save()
    url = reverse('matching_program:project', kwargs={"pk":project.id})
    return HttpResponseRedirect(url)

def remove_member(request, proj_pk, stu_pk):
    project = ResearchProject.objects.get(id=proj_pk)
    user = User.objects.get(id=stu_pk)
    project.members.remove(user)
    project.save()
    url = reverse('matching_program:project', kwargs={"pk":proj_pk})
    return HttpResponseRedirect(url)

@login_required
def student_app(request,pk):
    student = StudentApplication.objects.get(id=pk)
    return render(request, "matching_program/student.html",
                  context= {'student':student})


def add_student_app(request,pk):
    if request.method == "POST":
        if utils.is_new_application(request.user, pk):
            student_app = StudentApplication(user=request.user, research_id=pk)
            form = StudentApplicationForm(request.POST ,instance=student_app)
            if form.is_valid():
                form_object= form.save()
        url = reverse('matching_program:project', kwargs={"pk":pk})
        return HttpResponseRedirect(url)
    return render(request, "matching_program/edit_app_form.html",{"form":StudentApplicationForm, 'pk':pk})
    
def edit_app(request):
    pass

def delete_app(request,pk):
    app = StudentApplication.objects.get(id=pk)
    project_id= app.research.id
    app.delete()
    url = reverse('matching_program:project', kwargs={"pk":project_id})
    return HttpResponseRedirect(url)

# Create your views here.
