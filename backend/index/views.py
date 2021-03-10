from django.shortcuts import render
#from rest_framework_jwt.views import verify_jwt_token
#rom rest_framework_simplejwt.backends import TokenBackend
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.
from django.http import HttpResponse

class indexView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        path = request.path
        print(request.path)

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

def angularLogIn(request, path=''):
    """
    redirect to angular login page
    """
    return redirect(settings.VIEW_REDIRECT_URL + '/login')