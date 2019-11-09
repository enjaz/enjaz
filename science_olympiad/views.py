from django.shortcuts import render
from .models import Inventor
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
