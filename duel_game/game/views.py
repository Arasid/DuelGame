from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("DuelGame says hey there world!")

