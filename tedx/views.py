from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from clubs.models import Team
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

    return render(request, 'tedx/the_end.html', context)

@login_required
def list_registration(request):
    tedx_team = Team.objects.get(code_name="tedx_2017_registration")
    is_tedx_member = tedx_team.members.filter(pk=request.user.pk).exists() or\
                     tedx_team.coordinator == request.user
    if not request.user.is_superuser and\
       not is_tedx_member:
        raise PermissionDenied

    list_registration = Registration.objects.all()
    context = {'list_registration' : list_registration}
    return render(request, 'tedx/list_registration.html', context)
