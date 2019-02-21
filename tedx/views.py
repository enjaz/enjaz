from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators import csrf
from clubs.models import Team
from core import decorators
from .forms import RegistrationForm
from .models import Choice, Question, Game, Registration
from . import utils
from django.core.urlresolvers import reverse


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

@login_required
def list_registration(request):
    tedx_team = Team.objects.get(code_name="tedx_2017_registration")
    is_tedx_member = tedx_team.members.filter(pk=request.user.pk).exists() or\
                     tedx_team.coordinator == request.user
    if not request.user.is_superuser and\
       not is_tedx_member:
        raise PermissionDenied

    list_registration = Registration.objects.filter(submission__year=2019)
    context = {'list_registration' : list_registration}
    return render(request, 'tedx/list_registration.html', context)

def handle_game_index(request):
    game = Game.objects.order_by("?").first()
    first_question = game.first_question
    return render(request, "tedxgame/index.html",
                  {'first_question': first_question})

@csrf.csrf_exempt
@decorators.ajax_only
def handle_game_ajax(request):
    choice_pk = request.POST['choice_pk']
    choice = Choice.objects.get(pk=choice_pk)
    if choice.next_question.choices.exists():
        response= {"next_question_text": choice.next_question.question_text,
                   "choice1_text": choice.next_question.choices.first().choice_text,
                   "choice1_pk": choice.next_question.choices.first().pk,
                   "choice1_icon": choice.next_question.choices.first().icon,
                   "choice2_icon": choice.next_question.choices.last().icon,
                   "choice2_text": choice.next_question.choices.last().choice_text,
                   "choice2_pk": choice.next_question.choices.last().pk,
                   "flag": choice.flag}
    else:
        response = {"next_question_text": choice.next_question.question_text,
                    "flag": choice.flag}

    return response
