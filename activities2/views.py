from django.shortcuts import render
from django.forms import ModelForm
from activities2.models import Activity

def submission_activity(requset):
    if requset.method == 'POST':
        form = SubmissionForm(requset.POST)
        if form.is_valid:
            Activity_requset = form.save()
    else:
        form = SubmissionForm
    return render (requset,"",{"form":form})

class SubmissionForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['primary_club','secondary_clubs','chosen_reviewer_club','name','description','public_description',
                  'goals','requirements','submitter','submission_date','edit_date','is_editable','is_deleted',
                  'inside_collaborators','outside_collaborators','participants','category','organizers',
                  'assignee','gender','is_approved']

def activities_list_for_reviwer(request):
    context={
        "active":Activity.objects.all().filter(is_approved=None).current_year(),
        "inactive": Activities.objects.all().filter(is_approved=False, is_approved=True).current_year(),
        }
    if request.user.is_authenticated():
        template = "activities2/"

    return render(requests, template, context)

    
# Create your views here.
