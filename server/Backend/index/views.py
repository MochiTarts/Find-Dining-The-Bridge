from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request, path=''):
    path = request.path
    if path == '/all':
        content = "public content"
    elif path == '/user':
        content = "basic user content"
    elif path == '/ro':
        content = "restaurant owner content"
    else:
        content = "default content"
    return HttpResponse(content)
    #return render(request, 'index/landing-page.html')

