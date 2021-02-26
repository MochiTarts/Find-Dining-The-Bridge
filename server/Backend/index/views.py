from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request, path=''):
    path = request.path
    print(path)
    if path == '/api/all':
        content = "public content"
    elif path == '/api/user':
        content = "basic user content"
    elif path == '/api/ro':
        content = "restaurant owner content"
    else:
        content = "default content"
    return HttpResponse(content)

def angularIndex(request, path=''):
    return render(request, 'index/landing-page.html')

