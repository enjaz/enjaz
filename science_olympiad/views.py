from django.shortcuts import render, get_object_or_404
from .models import Inventor, Contest, ContestQuestion, ContestAnswer
from .forms import InventorForm


def index(request):
    return render(request, 'science_olympiad/index.html')

def view_form(request):
    return render(request, 'science_olympiad/view_form.html')

def view_section(request, section):
    context = {'section' : section}
    return render(request, 'science_olympiad/view_'+section+'.html', context)

def add_inventor(request):
    if request.method == 'POST':
        instance = Inventor()
        form = InventorForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save()
    elif request.method == 'GET':
        form = InventorForm()
    context = {'form': form}
    return render(request, 'science_olympiad/add_inventor.html', context)

def add_inventor2(request):
    if request.method == 'POST':
        instance = Inventor()
        form = InventorForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save()
    elif request.method == 'GET':
        form = InventorForm()
    context = {'form': form}
    return render(request, 'science_olympiad/add_inventor2.html', context)

def add_inventor3(request):
    if request.method == 'POST':
        instance = Inventor()
        form = InventorForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save()
    elif request.method == 'GET':
        form = InventorForm()
    context = {'form': form}
    return render(request, 'science_olympiad/add_inventor3.html', context)

def begin_contest(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    questions = ContestQuestion.objects.filter(contest=contest)
    context = {'contest':contest, 'questions':questions}
    return render(request, 'science_olympiad/begin_contest.html', context)

def show_contest_welcomepage(request, contest_id, question_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    questions = ContestQuestion.objects.filter(contest=contest)
    question = questions.get(pk=question_id)
    context = {'contest_id': contest_id, 'question':question,}
    return render(request, 'science_olympiad/show_contest_welcomepage.html', context)

def show_contest_endpage(request):
    return render(request, 'science_olympiad/show_contest_endpage.html')

def walkthrough_contest(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    questions = ContestQuestion.objects.filter(contest=contest)
    context = {'contest': contest, 'questions': questions}
    return render(request, 'science_olympiad/walkthrough_contest.html', context)

def handle_walkthrough(request, contest_id):
    contest = Contest.objects.get(pk=contest_id)
    question_pool = ContestQuestion.objects.filter(contest=contest)
    next_question = question_pool.first()
    if next_question:
        choices = []
        for choice in next_question.contestanswer_set.all():
            choice = {'pk': choice.pk,
                      'text': choice.text,}
            choices.append(choice)
        return {"question_text": next_question.text,
                "question_pk": next_question.pk,
                "choices": choices}
    else:
        return {'done': 1}

def walkthrough_contest1(request):
    contest = get_object_or_404(Contest, pk=1)
    questions = ContestQuestion.objects.filter(contest=contest)
    context = {'contest': contest, 'questions': questions}
    return render(request, 'science_olympiad/walkthrough_contest1.html', context)

def test_wheel(request):
    return render(request, 'science_olympiad/test_wheel.html')

# TODO: Fix this whole file
# the actual view for the game that works is show_question()

def show_question(request, contest_id, question_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    questions = ContestQuestion.objects.filter(contest=contest)
    question = questions.get(pk=question_id)
    choices = question.contestanswer_set.all()
    choice1 = choices.get(choice_letter='a')
    choice2 = choices.get(choice_letter='b')
    choice3 = choices.get(choice_letter='c')
    choice4 = choices.get(choice_letter='d')
    for choice in choices:
        if choice.is_correct:
            answer = choice
    excludables = question.contestanswer_set.filter(is_excludable=True)
    if len(list(excludables)) == 2:
        excludables = list(excludables)
        excludable_1 = excludables.pop()
        excludable_2 = excludables.pop()
    next_question_id = int(question_id) + 1
    context = {'contest': contest, 'questions': questions, 'question':question,
               'choice1':choice1, 'choice2':choice2,
               'choice3':choice3, 'choice4':choice4,
               'next_question_id':next_question_id, 'answer':answer,
               'excludable_1':excludable_1, 'excludable_2':excludable_2}
    return render(request, 'science_olympiad/show_question.html', context)