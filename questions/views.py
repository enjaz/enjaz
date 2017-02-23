# Create your views here

from questions.models import Question,QuestionFigure,Booth,Choice,Game
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators import csrf
from core import decorators
from django.shortcuts import render


def game_home(request):

    return render(request, 'the_game.html')


@decorators.ajax_only
@decorators.post_only
@csrf.csrf_exempt
@login_required
def toggle_new_game(request):

    game = Game.objects.create(user=request.user)
    game.save()

    results = {"game_pk": game.pk,
               "questions":[]
               }
    for booth in Booth.objects.all():
        questions = booth.question_set.all()
        for question in questions:
            options = question.choice_set.all()
            choices =[]
            text_result = []
            for choice in options:
                choices.append({"pk": choice.pk, "text": choice.text})
            if question.question_type == 'Q':
                text_result.append({"text": question.text})
            elif question.question_type == 'F':
                for image in question.question.questionfigure.figure_set.all():
                    text_result.append({"pk":image.pk,"image":image.url})
            elif question.question_type == 'S':
                text_result.append = ({"image":question.questionfigure.figure_set.first().url})
            question_result = {"type": question.question_type,
                               "pk": question.pk,
                               "choices": choices,
                               "text": question.text,
                               "content": text_result,
                               }
            results["questions"].append(question_result)

#            {"game_pk": game.pk,
#             "questions": [{type: "text",
#                           pk: 12,
#                           text: "Who did what?",
#                           choices: [{pk: 1, text: "you"}, {pk: 2, text: "i"}]
#             }

    return results











