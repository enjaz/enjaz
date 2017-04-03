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
            form.save()
            # If user is logged-in, let's try sending a tweet!
            if request.user.is_authenticated():
                relative_url = reverse('tedx:handle_registration')
                full_url = request.build_absolute_uri(relative_url)
                utils.create_tweet(request.user, full_url)

            return HttpResponseRedirect(reverse('tedx:thanks'))
    else:
        form = RegistrationForm()
    context = {'form': form}

    return render(request, 'tedx/index.html', context)
