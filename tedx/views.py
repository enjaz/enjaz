from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import RegistrationForm
from .models import Registration
import utils

def handle_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            # If user is logged-in, let's try sending a tweet!
            if request.user.is_authenticated():
                registration.user = request.user
                utils.create_tweet(request.user)
            registration.save()
            return HttpResponseRedirect(reverse('tedx:thanks'))
    else:
        form = RegistrationForm()
    context = {'form': form}

    return render(request, 'tedx/index.html', context)

def list_registration(request):
    list_registration = Registration.objects.all()
    context = {'list_registration' : list_registration}
    return render(request, 'tedx/list_registration.html', context)
