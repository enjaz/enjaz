from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def test(request):
    return HttpResponse("HPC 2020 Homepage.")