from django.shortcuts import render

# Create your views here.
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators import csrf
from .forms import NominationForm
from .models import Nomination

@login_required
def add_nominee(request):
    current_year ='2021-2022'
    user_nominations = Nomination.objects.filter(user=request.user)
    if user_nominations.exists():
        context = {'already_on': True}
        return HttpResponseRedirect('thanks/')
    if request.method == 'POST':
            instance = Nomination(user=request.user)
            form = NominationForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                instance = form.save()
                return HttpResponseRedirect('thanks/')
    elif request.method == 'GET':
            form = NominationForm()
    context = {'form' : form}

    return render(request,'voting/add_nominee.html', context)
