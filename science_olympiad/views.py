from django.shortcuts import render


def index(request):
    return render(request, 'science_olympiad/index.html')

def view_form(request):
    return render(request, 'science_olympiad/view_form.html')

def view_section(request, section):
    context = {'section' : section}
    return render(request, 'science_olympiad/view_'+section+'.html', context)
