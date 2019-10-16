# -*- coding: utf-8  -*-
from django.shortcuts import render

# Create your views here.
# enjazportal.com/riyadh/ar HPC Riyadh arabic and english homepage:
def riy_ar_index(request):
    context = {}
    return render(request,'newhpc/arabic/riy_ar_index.html',context)

def riy_en_index(request):
    context = {}
    return render(request,'newhpc/english/riy_en_index.html',context)


def riy_ar_research(request):
    context = {}
    return render(request,'newhpc/arabic/arabic_research.html',context)