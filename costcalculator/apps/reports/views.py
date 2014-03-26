#from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def reports_home(request):
    return HttpResponse('reports home')
