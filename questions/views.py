# -*- coding: utf-8  -*-

from questions.models import Question,QuestionFigure,Booth,Choice,Game
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators import csrf
from core import decorators
from django.shortcuts import render, get_object_or_404



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
        #questions =booth.question_set.order_by('?').first()
        for question in questions:
            options = question.choice_set.all()
            choices =[]
            text_result = []
            for choice in options:
                choices.append({"pk": choice.pk, "text": choice.text})
            if question.question_type == 'Q':
                text_result.append({"text": question.text})
            elif question.question_type == 'F':
                for image in question.questionfigure_set.all():
                    text_result.append({"image":image.figure.url})
            elif question.question_type == 'S':
                text_result.append({"image":question.questionfigure_set.first().figure.url})
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


@decorators.ajax_only
@decorators.post_only
@login_required
@csrf.csrf_exempt
def toggle_right_answer(request):
    choice_pk = request.POST.get('choice_pk')
    choice = get_object_or_404(Choice, pk=choice_pk)
    question_pk = request.POST.get('question_pk')
    question = get_object_or_404(Question,pk=question_pk)
    game_pk = request.POST.get('game_pk')
    game = get_object_or_404(Game, pk=game_pk)
    score = game.right_answers
    if choice.is_answer:
        right= True
    else:
        right = False
    return {"right":right,"score":score}













