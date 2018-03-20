from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from clubs.models import Club
from matching_program import utils
from models import ResearchProject, StudentApplication
from matching_program.forms import ResearchProjectForm, StudentApplicationForm


@login_required
def index(request, massage):
    my_projects = ResearchProject.objects.filter(creator= request.user)
    new_projects = ResearchProject.objects.filter(status="N")
    inProgress_projects = ResearchProject.objects.filter(status="IP")
    puplished_projects = ResearchProject.objects.filter(status="P")
    context= {"new_projects":new_projects,"inProgress_projects":inProgress_projects,
              "puplished_projects":puplished_projects, "massage":massage, "my_projects":my_projects}
    
    if utils.is_matchingProgram_coordinator_or_member(request.user) or\
       request.user.is_superuser:
        applied_projects = ResearchProject.objects.filter(status="A")
        context['applied_projects']=applied_projects
        
    return render(request, "matching_program/index.html",
                  context)

def coordinator_page(request):
    if utils.is_matchingProgram_coordinator(request.user) == False:
        return HttpResponseRedirect(reverse("matching_program:index"))
    return render(request, "matching_program/coordinator.html",{})

def members_list(request):
    matching_program_members = Club.objects.get(name="matching_program").members.all().values_list('id', flat=True)
    object_list = User.objects.filter(id__in=matching_program_members)
    json = serializers.serialize('json', object_list)
    return HttpResponse(json, content_type='application/json')


def search_ajax(request):
    matching_program_members = Club.objects.get(name="matching_program").members.all().values_list('id', flat=True)
    object_list = User.objects.exclude(id__in=matching_program_members)
    json = serializers.serialize('json', object_list)
    return HttpResponse(json, content_type='application/json')

def add_team(request, pk):
    user = User.objects.get(pk=pk)
    Club.objects.get(name="matching_program").members.add(user)
    return HttpResponseRedirect(reverse("matching_program:coordinator_page"))

def remove_team(request, pk):
    user = User.objects.get(pk=pk)
    Club.objects.get(name="matching_program").members.remove(user)
    return HttpResponseRedirect(reverse("matching_program:coordinator_page"))


    
def add_project(request):
    if request.method == 'POST':
        Project = ResearchProject(creator= request.user)
        form = ResearchProjectForm(request,request.POST, instance= Project)
        print form.errors
        if form.is_valid():
            form_object = form.save()
            return HttpResponseRedirect(reverse('matching_program:massage', kwargs={"massage":"success"}))
        return HttpResponseRedirect(reverse('matching_program:massage', kwargs={"massage":"fail"}))
    return render(request, "matching_program/edit_project_form.html",
                  {"form":ResearchProjectForm(request)})
    
@login_required
def project(request,pk, massage):
    project= ResearchProject.objects.get(id=pk)
    context={'project':project, 'form': StudentApplicationForm, "massage":massage}

    try:
        if StudentApplication.objects.get(research__id=pk,user=request.user):
            context['my_app']= StudentApplication.objects.get(research__id=pk,user=request.user)
    except :
        pass
    

    if utils.is_matchingProgram_coordinator_or_member(request.user) or\
       request.user.is_superuser:
        members = project.members.all
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
    return render(request, "matching_program/edit_form.html",
                  {'form':ResearchProjectForm(request, instance=project), "pk":pk})

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
        project= ResearchProject.objects.get(id=pk)
        if utils.is_new_application(request.user, pk):
            student_app = StudentApplication(user=request.user, research_id=pk)
            form = StudentApplicationForm(request.POST ,instance=student_app)
            if form.is_valid():
                form_object= form.save()
                url = reverse('matching_program:project_massage', kwargs={"pk":pk,"massage":"success"})
                return HttpResponseRedirect(url)
        url = reverse('matching_program:project_massage', kwargs={"pk":pk,"massage":"fail"})
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
