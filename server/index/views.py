from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request, path=''):
    return render(request, 'index/landing-page.html')
    #return HttpResponse("Hello, world. You're at the polls index.")