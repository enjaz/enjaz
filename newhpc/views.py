# -*- coding: utf-8  -*-
from django.shortcuts import render
from .models import FaqCategory, FaqQuestion
from .forms import FaqCategoryForm, FaqQuestionForm

# Create your views here.
# enjazportal.com/riyadh/ar HPC Riyadh arabic and english homepage:
"""
def riy_ar_index(request):
    context = {}
    return render(request,'newhpc/arabic/riy_ar_index.html',context)

def riy_en_index(request):
    context = {}
    return render(request,'newhpc/english/riy_en_index.html',context)
"""

def riy_en_research(request):
    context = {}
    return render(request,'newhpc/english/riy_en_research.html',context)

def show_about(request, lang):
    if lang == 'ar':
        lang2 = 'arabic'
    elif lang == 'en':
        lang2 = 'english'
    return render(request, 'newhpc/'+lang2+'/riy_'+lang+'_about.html')

def add_FaqCategory(request):
    if request.method == 'POST':
        instance = FaqCategory()
        form = FaqCategoryForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
    elif request.method == 'GET':
        form = FaqCategoryForm()
    context = {'form' : form}
    return render(request, 'newhpc/english/administrative/add_faq_category.html', context)

def add_FaqQuestion(request):
    if request.method == 'POST':
        instance = FaqQuestion()
        form = FaqQuestionForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
    elif request.method == 'GET':
        form = FaqQuestionForm()
    context = {'form' : form}
    return render(request, 'newhpc/english/administrative/add_faq_question.html', context)
