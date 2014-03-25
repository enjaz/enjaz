from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, this is the Niqati app!")

# Student Views

def submit(request, code):
    return HttpResponse("Thank you for submitting the code: %s" % code)

def student_report(request):
    return HttpResponse("This is your report: ...")

# Club Views

def create_codes(request):
    return HttpResponse("Your codes are being created.")

def view_orders(request):
    return HttpResponse("You have ordered lots of codes.")

# Management Views

def approve_codes(request):
    return HttpResponse("No idea requests up to the moment. Enjoy your day!")

def general_report(request):
    return HttpResponse("Here is a report of all students")