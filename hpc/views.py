from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse


from hpc.forms import AbstractForm, EvaluationForm
from hpc.models import Abstract, Evaluation
from hpc import utils

def submit_abstract(request):
    if request.method == 'POST':
        form = AbstractForm(request.POST, request.FILES)
        if form.is_valid():
            abstract = form.save()
            return HttpResponseRedirect(reverse('hpc:abstract_submision_completed'))

    elif request.method == 'GET':
        form = AbstractForm()

    return render(request, 'hpc/abstract_submission.html', {'form': form})

@login_required
def list_abstracts(request):
    if not utils.is_research_committee_member(request.user) and \
       not utils.is_organizing_committee_member(request.user) and \
       not request.user.is_superuser:
        raise PermissionDenied

    pending_abstracts = Abstract.objects.filter(is_deleted=False, evaluation__isnull=True)
    evaluated_abstracts = Abstract.objects.filter(is_deleted=False, evaluation__isnull=False)

    # The Research Committee is only concerned about abstracts from
    # the university.  The rest will be evaluated by the Organizing
    # Committee.
    if utils.is_research_committee_member(request.user):
        pending_abstracts = pending_abstracts.filter(university="KSAU-HS")
        evaluated_abstracts = evaluated_abstracts.filter(university="KSAU-HS")
    elif utils.is_organizing_committee_member(request.user):
        pending_abstracts = pending_abstracts.exclude(university="KSAU-HS")
        evaluated_abstracts = evaluated_abstracts.exclude(university="KSAU-HS")

    context = {'pending_abstracts': pending_abstracts,
               'evaluated_abstracts': evaluated_abstracts}

    return render(request, 'hpc/list_abstracts.html', context)

@login_required
def show_abstract(request, pk):
    if not utils.is_research_committee_member(request.user) and \
       not utils.is_organizing_committee_member(request.user) and \
       not request.user.is_superuser:
        raise PermissionDenied

    abstract = get_object_or_404(Abstract, pk=pk, is_deleted=False)
    try:
        evaluation = abstract.evaluation
    except Evaluation.DoesNotExist:
        evaluation = Evaluation(evaluator=request.user,
                                abstract=abstract)

    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('hpc:list_abstracts'))
    elif request.method == 'GET':
        form = EvaluationForm(instance=evaluation)

    return render(request, "hpc/show_abstract.html",
                  {'abstract': abstract, 'form': form})
