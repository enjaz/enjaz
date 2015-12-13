from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from hpc.forms import AbstractForm
from hpc.models import Abstract


def submit_abstract(request):
    if request.method == 'POST':
        form = AbstractForm(request.POST, request.FILES)
        if form.is_valid():
            abstract = form.save()
            return HttpResponseRedirect(reverse('hpc:abstract_submision_completed'))

    elif request.method == 'GET':
        form = AbstractForm()

    return render(request, 'hpc/abstract_submission.html', {'form': form})
