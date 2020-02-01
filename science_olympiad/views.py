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

def show_contest_welcomepage(request, contest_id):
    context = {'contest_id': contest_id}
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