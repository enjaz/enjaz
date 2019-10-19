# -*- coding: utf-8  -*-
from django.shortcuts import render

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
    # return render(request, 'newhpc/english/riy_en_about.html')